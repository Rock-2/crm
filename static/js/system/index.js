/**
 * Created by 磊 on 2018/10/26.
 */

function system_index_update_password_dialog() {


    $('#system_index_update_password_dialog').dialog({
        title: '修改密码',
        closed: true,//是否关闭
        href: 'get_content.php',
        modal: true,//模态
        iconCls: 'icon-edit',
        resizable: false,//定义是否能够改变窗口大小
        draggable: false, // 不可移动
        width: 260,
        buttons: [{  // 按钮
            text: '保存',
            iconCls: 'icon-save',
            handler: function () {
                var flag = $('#system_index_update_password_form').form('validate');
                if (flag) {
                    // 提交表单
                    sub_system_index_updatepwd_form();

                    // 清除form表单input
                    $('#system_index_update_password_form input').val('');

                    // 关闭修改密码dialog
                    $('#system_index_update_password_dialog').dialog('close');
                }
            }
        }, {
            text: '关闭',
            iconCls: 'icon-cancel',
            handler: function () {
                $('#system_index_update_password_dialog').dialog('close');
            }
        }]
    });
}
// 点击修改密码弹出对话框
function open_update_password_dialog(username) {
    // 返显用户名
    $('#username').val(username);
    $('#system_index_update_password_dialog').dialog('open');
}