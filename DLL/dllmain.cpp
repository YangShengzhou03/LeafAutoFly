#include "pch.h"
#include <string>
#include <unordered_map>
#include <functional>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <http.h>
#include <fstream>
#include <thread>
#include <chrono>
#include <atomic>
#include <memory>
#include <vector>

#pragma comment(lib, "httpapi.lib")
#pragma comment(lib, "Ws2_32.lib")

#include "third_party/json-develop/single_include/nlohmann/json.hpp"

using json = nlohmann::json;

// 前向声明
class WxStruct;
bool SendText(const json& jsonData);

// RAII包装器
namespace RAII {
    struct HttpHandle {
        HANDLE handle = NULL;
        explicit HttpHandle(HANDLE h = NULL) : handle(h) {}
        ~HttpHandle() { if (handle) CloseHandle(handle); }
    };

    struct HeapMem {
        void* ptr = nullptr;
        explicit HeapMem(size_t size) : ptr(HeapAlloc(GetProcessHeap(), 0, size)) {}
        ~HeapMem() { if (ptr) HeapFree(GetProcessHeap(), 0, ptr); }
    };
}

// 全局原子标志用于线程控制
std::atomic<bool> g_running(true);

// 微信功能相关常量
namespace WeChatSendText {
    constexpr DWORD64 WECHAT_DLL_OFFSET = 0x22D4A90;
    constexpr const char* WECHAT_DLL_NAME = "WeChatWin.dll";
}

// 安全字符串转换
std::wstring StringToWide(const std::string& str) {
    if (str.empty()) return L"";
    int size = MultiByteToWideChar(CP_UTF8, 0, str.c_str(), (int)str.size(), nullptr, 0);
    std::wstring wstr(size, 0);
    MultiByteToWideChar(CP_UTF8, 0, str.c_str(), (int)str.size(), &wstr[0], size);
    return wstr;
}

// 改进的WxStruct类
class WxStruct {
public:
    std::unique_ptr<wchar_t[]> pStr;
    DWORD minLen = 0;
    DWORD maxLen = 0;
    DWORD64 full1 = 0, full2 = 0, full3 = 0;

    explicit WxStruct(const std::wstring& str) {
        size_t len = str.length() + 1;
        pStr.reset(new wchar_t[len]);
        wcscpy_s(pStr.get(), len, str.c_str());
        minLen = static_cast<DWORD>(str.length());
        maxLen = minLen * 2;
    }
};

// HTTP服务器封装类
class HttpServer {
public:
    HttpServer() : m_version{ 2, 0 } {}

    bool Initialize() {
        if (HttpInitialize(m_version, HTTP_INITIALIZE_SERVER, NULL) != NO_ERROR)
            return false;

        if (HttpCreateRequestQueue(m_version, NULL, NULL, 0, &m_requestQueue.handle) != NO_ERROR)
            return false;

        return SetupUrlGroup();
    }

    void Run() {
        constexpr ULONG initialBufferSize = 4096;
        std::vector<BYTE> buffer(initialBufferSize);

        while (g_running) {
            HTTP_REQUEST* pRequest = reinterpret_cast<HTTP_REQUEST*>(buffer.data());
            ULONG bytesRead = 0;

            ULONG result = HttpReceiveHttpRequest(
                m_requestQueue.handle,
                HTTP_NULL_ID,
                HTTP_RECEIVE_REQUEST_FLAG_COPY_BODY,
                pRequest,
                static_cast<ULONG>(buffer.size()),
                &bytesRead,
                NULL
            );

            if (result == ERROR_MORE_DATA) {
                buffer.resize(bytesRead);
                continue;
            }

            if (result == NO_ERROR) {
                HandleRequest(pRequest);
            }
            else if (!g_running) {
                break;
            }
        }
    }

private:
    HTTPAPI_VERSION m_version{ 2, 0 };
    RAII::HttpHandle m_requestQueue;
    HTTP_SERVER_SESSION_ID m_serverSessionId = 0;
    HTTP_URL_GROUP_ID m_urlGroupId = 0;

    bool SetupUrlGroup() {
        if (HttpCreateServerSession(m_version, &m_serverSessionId, 0) != NO_ERROR)
            return false;

        if (HttpCreateUrlGroup(m_serverSessionId, &m_urlGroupId, 0) != NO_ERROR) {
            HttpCloseServerSession(m_serverSessionId);
            return false;
        }

        if (HttpAddUrlToUrlGroup(m_urlGroupId, L"http://localhost:8080/", 0, 0) != NO_ERROR) {
            HttpCloseUrlGroup(m_urlGroupId);
            HttpCloseServerSession(m_serverSessionId);
            return false;
        }

        HTTP_BINDING_INFO bindingInfo = {};
        bindingInfo.RequestQueueHandle = m_requestQueue.handle;
        bindingInfo.Flags.Present = TRUE;

        return HttpSetUrlGroupProperty(m_urlGroupId,
            HttpServerBindingProperty,
            &bindingInfo,
            sizeof(bindingInfo)) == NO_ERROR;
    }

    void HandleRequest(HTTP_REQUEST* pRequest) {
        std::string method;
        switch (pRequest->Verb) {
        case HttpVerbGET: method = "GET"; break;
        case HttpVerbPOST: method = "POST"; break;
        default: method = "UNKNOWN"; break;
        }

        std::wstring urlPathW(pRequest->CookedUrl.pFullUrl + wcslen(L"http://localhost:8080"),
            pRequest->CookedUrl.FullUrlLength / sizeof(WCHAR) - wcslen(L"http://localhost:8080"));
        std::string urlPath(urlPathW.begin(), urlPathW.end());

        std::unordered_map<std::string, std::function<bool(const json&)>> handlers = {
            {"/api/sendtext", SendText}
        };

        HTTP_RESPONSE response = {};
        response.StatusCode = 200;
        response.pReason = "OK";
        response.ReasonLength = (USHORT)strlen(response.pReason);

        std::string responseBody;
        try {
            if (method == "POST" && handlers.find(urlPath) != handlers.end()) {
                std::vector<char> requestBodyBuffer(4096);
                ULONG bytesRead = 0;
                HttpReceiveRequestEntityBody(m_requestQueue.handle,
                    pRequest->RequestId,
                    0,
                    requestBodyBuffer.data(),
                    static_cast<ULONG>(requestBodyBuffer.size()),
                    &bytesRead,
                    NULL);

                json jsonData = json::parse(requestBodyBuffer.data());
                bool sendResult = handlers[urlPath](jsonData);
                responseBody = sendResult ?
                    R"({"status":"success", "message":"Message sent successfully"})" :
                    R"({"status":"error", "message":"Failed to send message"})";
            }
            else {
                responseBody = R"({"status":"error", "message":"Invalid request"})";
            }
        }
        catch (const std::exception& e) {
            responseBody = R"({"status":"error", "message":")" + std::string(e.what()) + "\"}";
        }

        HTTP_DATA_CHUNK dataChunk;
        dataChunk.DataChunkType = HttpDataChunkFromMemory;
        dataChunk.FromMemory.pBuffer = (PVOID)responseBody.data();
        dataChunk.FromMemory.BufferLength = (ULONG)responseBody.size();

        response.Headers.KnownHeaders[HttpHeaderContentType].pRawValue = "application/json";
        response.Headers.KnownHeaders[HttpHeaderContentType].RawValueLength = 16;
        response.EntityChunkCount = 1;
        response.pEntityChunks = &dataChunk;

        HttpSendHttpResponse(m_requestQueue.handle,
            pRequest->RequestId,
            0,
            &response,
            NULL,
            NULL,
            NULL,
            0,
            NULL,
            NULL);
    }
};

// 微信消息发送函数
bool SendText(const json& jsonData) {
    try {
        std::string who = jsonData.at("who").get<std::string>();
        std::string msg = jsonData.at("msg").get<std::string>();

        WxStruct wxid(StringToWide(who));
        WxStruct message(StringToWide(msg));

        HMODULE hModule = LoadLibraryA(WeChatSendText::WECHAT_DLL_NAME);
        if (!hModule) {
            OutputDebugStringA("Failed to load WeChat DLL");
            return false;
        }

        auto CallFunc = reinterpret_cast<DWORD64(*)(...)>(
            reinterpret_cast<DWORD64>(hModule) + WeChatSendText::WECHAT_DLL_OFFSET
            );

        char buf1[0x18] = { 0 };
        char buf2[0x1024] = { 0 };

        CallFunc(&buf2, &wxid, &message, &buf1, 1, 1, 0, 0);
        return true;
    }
    catch (const std::exception& e) {
        OutputDebugStringA(e.what());
        return false;
    }
}

// 发送TCP消息函数
bool SendTOClient(const std::string& message) {
    WSADATA wsaData;
    SOCKET ConnectSocket = INVALID_SOCKET;
    struct sockaddr_in serverAddr;

    // 初始化Winsock
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        OutputDebugStringA("Failed to initialize Winsock.");
        return false;
    }

    // 创建套接字
    ConnectSocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (ConnectSocket == INVALID_SOCKET) {
        OutputDebugStringA("Error at socket():");
        WSACleanup();
        return false;
    }

    // 设置服务器地址信息
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(20042); // 端口号直接写死

    // 使用 inet_pton 替代 inet_addr
    if (inet_pton(AF_INET, "127.0.0.1", &serverAddr.sin_addr) != 1) { // IP地址直接写死
        OutputDebugStringA("Invalid address/ Address not supported.");
        closesocket(ConnectSocket);
        WSACleanup();
        return false;
    }

    // 连接到服务器
    if (connect(ConnectSocket, (struct sockaddr*)&serverAddr, sizeof(serverAddr)) == SOCKET_ERROR) {
        OutputDebugStringA("Failed to connect to server.");
        closesocket(ConnectSocket);
        WSACleanup();
        return false;
    }

    // 发送数据
    if (send(ConnectSocket, message.c_str(), static_cast<int>(message.length()), 0) == SOCKET_ERROR) {
        OutputDebugStringA("Send failed.");
        closesocket(ConnectSocket);
        WSACleanup();
        return false;
    }

    // 关闭套接字
    closesocket(ConnectSocket);
    WSACleanup();

    return true;
}

// 周期发送线程
void PeriodicSendText() {
    while (g_running) {
        // 准备要发送的消息
        json jsonData;
        jsonData["who"] = "filehelper";
        jsonData["msg"] = "Hello";

        // 调用SendText发送消息
        bool sendResult = SendText(jsonData);

        // 将JSON对象序列化为字符串
        std::string message = jsonData.dump();

        // 调用SendTOClient发送消息到指定的IP和端口
        bool sendToClientResult = SendTOClient(message);

        if (!sendResult || !sendToClientResult) {
            OutputDebugStringA("Failed to send messages.");
        }

        // 暂停10秒后再次发送
        std::this_thread::sleep_for(std::chrono::seconds(10));
    }
}

// DLL入口点
BOOL APIENTRY DllMain(HMODULE hModule, DWORD reason, LPVOID lpReserved) {
    switch (reason) {
    case DLL_PROCESS_ATTACH: {
        try {
            static HttpServer server;
            if (!server.Initialize()) return FALSE;

            std::thread([] { server.Run(); }).detach();
            std::thread(PeriodicSendText).detach();
        }
        catch (...) {
            return FALSE;
        }
        break;
    }
    case DLL_PROCESS_DETACH:
        g_running = false;
        std::this_thread::sleep_for(std::chrono::milliseconds(100)); // 等待线程退出
        break;
    }
    return TRUE;
}