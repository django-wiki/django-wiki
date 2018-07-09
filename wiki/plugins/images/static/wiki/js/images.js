$(document).ready(function() {
  $('.wiki-article .thumbnail').each(function() {
    caption = $(this).children('.caption').html();
    $(this).children('a').colorbox({width:"75%", height:"75%", title: caption})
  });
});
