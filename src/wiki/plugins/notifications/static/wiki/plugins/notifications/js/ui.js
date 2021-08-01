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
        $('.notification-cnt').addClass('badge-important');
      } else {
        $('.notification-cnt').removeClass('badge-important');
      }
      for (var i=data.objects.length-1; i >=0 ; i--) {
        n = data.objects[i];
        notify_latest_id = n.pk>notify_latest_id ? n.pk:notify_latest_id;
        notify_oldest_id = (n.pk<notify_oldest_id || notify_oldest_id==0) ? n.pk:notify_oldest_id;
        if (n.occurrences > 1) {
          element = $('<div><a href="'+URL_NOTIFY_GOTO+n.pk+'/"><div>'+n.message+'</div><div class="since">'+n.occurrences_msg+' - ' + n.since + '</div></a></div>')
        } else {
          element = $('<div><a href="'+URL_NOTIFY_GOTO+n.pk+'/"><div>'+n.message+'</div><div class="since">'+n.since+'</div></a></div>');
        }
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
