from wxautox import WeChat

wx = WeChat()


def send_msg(who, msg):
    wx.SendMsg(who=who, msg=msg)
