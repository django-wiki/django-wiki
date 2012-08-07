notify_latest_id = 0;

function notify_update() {
  jsonWrapper(URL_NOTIFY_GET_NEW, function (data) {
    if (data.success) {
      $('.notification-cnt').html(data.objects.length);
      if (data.objects.length> 0) {
        $('.notification-cnt').addClass('badge-important');
        $('.notifications-empty').hide();
      } else {
        $('.notification-cnt').removeClass('badge-important');
      }
      for (var i=0; i < data.objects.length; i++) {
        n = data.objects[i];
        notify_latest_id = n.pk>notify_latest_id ? n.pk:notify_latest_id;
        $('.notification-li-container').prepend($('<li><a href="'+URL_NOTIFY_GOTO+n.pk+'/"><div>'+n.message+'</div><div class="since">'+n.since+'</div></a></li>'))
      }
    }
  });
}

function notify_mark_read() {
  url = URL_NOTIFY_MARK_READ+notify_latest_id+'/';
  jsonWrapper(url, function (data) {
    if (data.success) {
      notify_update();
    }
  });
}

$(document).ready(function () {
  notify_update();
  // Update every second minute.
  setInterval("notify_update()", 120000);
})

