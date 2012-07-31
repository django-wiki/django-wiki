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
    alert(data.opcodes);
    put_in_element.find('.diff-container').empty();
    $(put_in_element).find('.diff-container').append(diffview.buildView({
      baseTextLines: data.baseTextLines,
      newTextLines: data.newTextLines,
      opcodes: data.opcodes,
      baseTextName: data.baseTextName,
      newTextName: data.newTextName,
      contextSize: 0,
      viewType: 0
    }));
    put_in_element.find('.diff-container').show('fast', function() {put_in_element.collapse('show');});
    alert(put_in_element.find('.diff-container').html());
  });
}
