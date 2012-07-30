function ajaxError(){}

$.ajaxSetup({
  timeout: 7000,
  cache: false,
  error: function(e, xhr, settings, exception) {
      ajaxError();
  }
});

function jsonWrapper(url, callback) {
  if (failureTimeoutSet)
    return;
  $.getJSON(url, function(data) {
    if (data == null) {
      ajaxError();
    } else {
      callback(data);
    }
  });
}

function diffUsingPython(url, put_in_element) {
  jsonWrapper(url, function (data) {
    try {
      while (diffoutputdiv.firstChild) diffoutputdiv.removeChild(diffoutputdiv.firstChild);
      $(put_in_element).appendChild(diffview.buildView({
        baseTextLines: data.baseTextLines,
        newTextLines: data.newTextLines,
        opcodes: data.opcodes,
        baseTextName: data.baseTextName,
        newTextName: data.newTextName,
        contextSize: contextSize
      }));
    } catch (ex) {
      alert("An error occurred updating the diff view:\n" + ex.toString());
    }
  }
}
