import "bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import "open-iconic/font/css/open-iconic-bootstrap.css";
import feather from "feather-icons";
import smoothscroll from 'smoothscroll-polyfill';
import "moment";

smoothscroll.polyfill();

import "../css/style.styl";

feather.replace();


function setNotificationRead() {
    
}



function appendNotificationItems(item) {
    $('#notificationBody').append(
        `<div class="row content-row">
            <div class="col-12 content-item notification-item" style="margin-bottom: 1px!important;">
                <div class="pl-1 pr-2 mr-1 notification-status">
                    <span class="notification-unread"></span>
                </div>
                <div class="flex-fill d-inline-flex justify-content-between">
                    <div>
                        ${item}
                    </div>
                    <!--<a href="javascript:void(0);" onclick="setNotificationRead()">read</a>-->
                </div>
            </div>
        </div>`
    );
}


function getUnreadNotifications() {
    $.ajax({
        url: '/ajax/notifications',
        dataType: 'json',
        success: function (data) {
            if (data && data.length > 0) {
                data.forEach(function (d) {
                    appendNotificationItems(d)
                });
            }
        }
    })
}



$("#notificationLink").click(function () {
    $("#messagePanel").addClass("d-none");
    if ($("#notificationPanel").hasClass("d-none")) {
        $("#notificationPanel").removeClass("d-none");
        if ($('#notificationBody').children().length == 0) {
            getUnreadNotifications();
        }

    } else {
        $("#notificationPanel").addClass("d-none");
    }
});

$("#messageLink").click(function () {
    $("#notificationPanel").addClass("d-none");
    if ($("#messagePanel").hasClass("d-none")) {
        $("#messagePanel").removeClass("d-none");
        $.ajax({
            url: '/ajax/notifications'
        })
    } else {
        $("#messagePanel").addClass("d-none");
    }
});

