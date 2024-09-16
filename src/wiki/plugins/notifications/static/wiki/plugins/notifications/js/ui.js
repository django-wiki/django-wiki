notify_oldest_id = 0;
notify_latest_id = 0;
notify_update_timeout = 30000;
notify_update_timeout_adjust = 1.2; // factor to adjust between each timeout.

function notify_update() {
  jsonWrapper(URL_NOTIFY_GET_NEW+notify_latest_id+'/', function (data) {
    if (data.success) {
      $('.notification-cnt').html(data.total_count);
      if (data.objects.length> 0) {
        $('.notifications-empty').hide();
      }
      if (data.total_count > 0) {
        $('.notification-cnt').addClass('bg-primary');
        $('.notification-cnt').removeClass('bg-secondary');
      } else {
        $('.notification-cnt').addClass('bg-secondary');
        $('.notification-cnt').removeClass('bg-primary');
      }
      for (var i=data.objects.length-1; i >=0 ; i--) {
        n = data.objects[i];
        notify_latest_id = n.pk>notify_latest_id ? n.pk:notify_latest_id;
        notify_oldest_id = (n.pk<notify_oldest_id || notify_oldest_id==0) ? n.pk:notify_oldest_id;
        var element_outer_div = $("<div />");
        var element_a = $("<a />", {href: URL_NOTIFY_GOTO + n.pk + "/"});
        var element_message_div;
        var element_since_div;
        if (n.occurrences > 1) {
          element_message_div = $("<div />", {text: n.message});
          element_since_div = $("<div />", {text: n.occurrences_msg+' - ' + n.since, class: "since"});
        } else {
          element_message_div = $("<div />", {text: n.message});
          element_since_div = $("<div />", {text: n.since, class: "since"});
        }
        element_a.append(element_message_div).append(element_since_div);
        element = element_outer_div.append(element_a);
        element.addClass('dropdown-item notification-item');
        element.insertAfter('.notification-before-list');
      }
    }
  });
}

function notify_mark_read() {
  $('.notification-item').remove();
  $('.notifications-empty').show();
  url = URL_NOTIFY_MARK_READ+notify_latest_id+'/'+notify_oldest_id+'/';
  notify_oldest_id = 0;
  notify_latest_id = 0;
  jsonWrapper(url, function (data) {
    if (data.success) {
      notify_update();
    }
  });
}

function update_timeout() {
  setTimeout("notify_update()", notify_update_timeout);
  setTimeout("update_timeout()", notify_update_timeout);
  notify_update_timeout *= notify_update_timeout_adjust;
}

$(document).ready(function () {
  update_timeout();
});

// Don't check immediately... some users just click through pages very quickly.
setTimeout("notify_update()", 2000);
