// 当页面加载完成后执行
$(document).ready(function() {
    // 获取客户选择框和订单选择框
    var clientSelect = $('#id_client');
    var orderSelect = $('#id_order');
    
    // 保存原始的订单选项
    var originalOrderOptions = orderSelect.html();
    
    // 当客户选择发生变化时
    clientSelect.change(function() {
        var clientId = $(this).val();
        
        // 如果没有选择客户，恢复所有订单选项
        if (!clientId) {
            orderSelect.html(originalOrderOptions);
            return;
        }
        
        // 清空当前订单选项
        orderSelect.html('<option value="">---------</option>');
        
        // 发送AJAX请求获取该客户的订单
        $.ajax({
            url: '/sample/get_orders/',
            type: 'GET',
            data: { 'client_id': clientId },
            dataType: 'json',
            success: function(data) {
                // 添加获取到的订单选项
                $.each(data.orders, function(index, order) {
                    orderSelect.append('<option value="' + order.id + '">' + order.name + ' (ID: ' + order.order_id + ')</option>');
                });
            },
            error: function(xhr, status, error) {
                console.log('获取订单失败:', error);
                console.log('状态:', status);
                console.log('响应:', xhr.responseText);
            }
        });
    });
});