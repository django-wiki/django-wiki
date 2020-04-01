$(".wiki-card-toggle").on("click", function(){
  var revision = this.dataset.revision;
  var url = this.dataset.jsonUrl;
  var put_in_element = "#collapse"+revision;

  if ($(put_in_element).find('.diff-container tbody').length === 0) {
    jsonWrapper(url, function (data) {

      $(put_in_element).parent().find('.progress').show(0 , function() {
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
        $(put_in_element).find('.diff-container').show('fast', function() {$(put_in_element).collapse('show');});
        $(put_in_element).parent().find('.progress').detach();
      });
    });
  }else {
    $(put_in_element).find('.diff-container').show('fast', function() {$(put_in_element).collapse('toggle');});
  }
});
