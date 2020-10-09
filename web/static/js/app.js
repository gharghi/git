$(document).foundation()
$(function () {
  var showClass = 'show';

  $('textarea, input').on('checkval', function () {
    var label = $(this).prev('label');
    if(this.value !== '') {
      label.addClass(showClass);
    } else {
      label.removeClass(showClass);
    }
  }).on('keyup', function () {
    $(this).trigger('checkval');
  });
});
$("[data-circle-graph]").each(function() {
  var $graph = $(this),
      percent = parseInt($graph.data('percent'), 10),
      deg = 360*percent/100;
  if(percent > 50) {
    $graph.addClass('gt-50');
  }
  $graph.find('.circle-graph-progress-fill').css('transform','rotate('+ deg +'deg)');
  $graph.find('.circle-graph-percents-number').html(percent+'%');
});
$('[data-open-details]').click(function (e) {
  e.preventDefault();
  $(this).next().toggleClass('is-active');
  $(this).toggleClass('is-active');
});
