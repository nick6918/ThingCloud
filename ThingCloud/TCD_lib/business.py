# -*- coding: utf-8 -*-

from TCD_lib.settings import PICURL, UPYUNURL


html_head = u"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>订单详情</title>
    <style>
        .info {
            color: blue;
            text-decoration: underline;
        }
    </style>
</head>
<body>

    """
html_tail =u"""

</body>
</html>
"""
def generateInfo(order, state):
    typeid = order.typeid
    html_text = u""
    if state < 2 or state >= 12:
        html_text += u"  <p>系统正在处理您的订单, 请稍候查看。</p>\n"
    elif state == 2:
        html_text += u"  <p>您的订单已创建, 正由<span class=info>"+order.addr.community_belong.wh_in.name+u"</span>处理中。</p>\n"
        if typeid == 0:
            html_text += u"  <p>正在等待快递员出单, 预计30分钟内前往<span class=info>"+order.addr.name+u"</span>取件。</p>\n"
            html_text += u"  <p>请准备好您要存入邻仓的物品， 快递员会上门取件并向您出具存货确认单。</p>\n"
        else:
            html_text += u"  <p>正在等待快递员出单, 预计30分钟内即将您的订单送至<span class=info>"+order.addr.name+u"。</span></p>\n"
    elif state==3:
        html_text = html_text + generateInfo(order, 2)
        if typeid == 0:
            try:
                html_text += u"  <p>快递员<span class=info>"+order.courier.worker.name+u"("+order.courier.worker.phone+u")</span>已出单, 预计20分钟内将您的订单送至<span class=info>"+order.addr.name+u"</span>。</p>\n"
            except Exception,e :
                html_text += u"  <p>快递员已出单, 预计20分钟内前往<span class=info>"+order.addr.name+u"</span>取件。</p>\n"              
        else:
            try:
                html_text += u"  <p>快递员<span class=info>"+order.courier.worker.name+u"("+order.courier.worker.phone+u")</span>已出单, 预计20分钟内将您的订单送至<span class=info>"+order.addr.name+u"</span>。</p>\n"
            except Exception,e :
                html_text += u"  <p>快递员已出单, 预计20分钟内将您的订单送至<span class=info>"+order.addr.name+u"</span>。</p>\n"              
    elif state==4:
        html_text = html_text + generateInfo(order, 3)
        html_text += u"  <p>快递员已取到货品, 预计1小时内送货入库。货品入库后, 您可在订单页面或者邻仓主页查看所有您存入的商品。</p>\n"
    elif state==5:
        if typeid == 0:
            html_text = html_text + generateInfo(order, 4)
            html_text += u"  <p>快递员已上传存货单, <a href="+PICURL+str(order.oid)+ u".png >点此查看</a>。</p>\n"
            html_text += u"  <p>存货成功，快递员已上传全部商品， 请前往主页确认。如有疑问, 请联系客服。</p>\n"
        else:
            html_text = html_text + generateInfo(order, 3)
            html_text += u"  <p>快递员已上传存货单, <a href="+PICURL+str(order.oid)+ u".png >点此查看</a>。</p>\n"
            html_text += u"  <p>取件成功， 快递员已将商品送至指定地址， 请您确认。如有疑问, 请联系客服。</p>\n"
    elif state == 7 or state == 8:
        html_text = html_text + generateInfo(order, 3)
        html_text += u"  <p>您的订单已取消。如有疑问, 请联系客服。</p>\n"
    elif state == 9:
        html_text = html_text + generateInfo(order, 5)
        html_text += u"  <p>系统已收到您的申诉请求, 我们将于1天内与您取得联系。</p>\n"
    elif state == 6:
        html_text = html_text + generateInfo(order, 5)
        html_text += u"  <p>您已确认订单无误， 订单完成。谢谢您的使用。</p>\n"
    else:
        html_text = html_text + generateInfo(order, 3)
        html_text += u"  <p>您的订单已取消。如有疑问, 请联系客服。</p>\n"
    return html_text