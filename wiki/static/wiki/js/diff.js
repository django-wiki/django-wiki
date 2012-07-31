function ajaxError(){}

$.ajaxSetup({
  timeout: 7000,
  cache: false,
  error: function(e, xhr, settings, exception) {
      ajaxError();
  }
});

function jsonWrapper(url, callback) {
  $.getJSON(url, function(data) {
    if (data == null) {
      ajaxError();
    } else {
      callback(data);
    }
  });
}

function get_diff_json(url, put_in_element) {
  jsonWrapper(url, function (data) {
    if (!$(put_in_element).find('.diff-container tbody').length > 0) {
      $(put_in_element).parentsUntil('.accordion').find('.progress').show(0 , function() {
        tbody = pydifferviewer.as_tbody({differ_output: data.diff});
        $(put_in_element).find('.diff-container table').append(
          tbody
        );
        if (data.other_changes) {
          for (var i=0; i < data.other_changes.length; i++) {
            $(put_in_element).find('dl').append($('<dt>'+data.other_changes[i][0]+'</dt>' +
                                                  '<dd>'+data.other_changes[i][1]+'</dd>'  ));
          }
        }        
        put_in_element.find('.diff-container').show('fast', function() {put_in_element.collapse('show');});
        $(put_in_element).parentsUntil('.accordion').find('.progress').detach();
      });
    } else {
      put_in_element.find('.diff-container').show('fast', function() {put_in_element.collapse('toggle');});
    }
  });
}
