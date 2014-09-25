$(document).ready(function()
{
	$("#navigation-container .article-list").sticky({topSpacing:95});
});

// Sticky Plugin v1.0.0 for jQuery
// =============
// Author: Anthony Garand
// Improvements by German M. Bravo (Kronuz) and Ruud Kamphuis (ruudk)
// Improvements by Leonardo C. Daronco (daronco)
// Created: 2/14/2011
// Date: 2/12/2012
// Website: http://labs.anthonygarand.com/sticky
// Description: Makes an element on the page stick on the screen as you scroll
//       It will only set the 'top' and 'position' of your element, you
//       might need to adjust the width in some cases.

(function(e){var t={topSpacing:0,bottomSpacing:0,className:"is-sticky",wrapperClassName:"sticky-wrapper",center:false,getWidthFrom:"",responsiveWidth:false},n=e(window),r=e(document),i=[],s=n.height(),o=function(){var t=n.scrollTop(),o=r.height(),u=o-s,a=t>u?u-t:0;for(var f=0;f<i.length;f++){var l=i[f],c=l.stickyWrapper.offset().top,h=c-l.topSpacing-a;if(t<=h){if(l.currentTop!==null){l.stickyElement.css("position","").css("top","");l.stickyElement.trigger("sticky-end",[l]).parent().removeClass(l.className);l.currentTop=null}}else{var p=o-l.stickyElement.outerHeight()-l.topSpacing-l.bottomSpacing-t-a;if(p<0){p=p+l.topSpacing}else{p=l.topSpacing}if(l.currentTop!=p){l.stickyElement.css("position","fixed").css("top",p);if(typeof l.getWidthFrom!=="undefined"){l.stickyElement.css("width",e(l.getWidthFrom).width())}l.stickyElement.trigger("sticky-start",[l]).parent().addClass(l.className);l.currentTop=p}}}},u=function(){s=n.height();for(var t=0;t<i.length;t++){var r=i[t];if(typeof r.getWidthFrom!=="undefined"&&r.responsiveWidth===true){r.stickyElement.css("width",e(r.getWidthFrom).width())}}},a={init:function(n){var r=e.extend({},t,n);return this.each(function(){var n=e(this);var s=n.attr("id");var o=s?s+"-"+t.wrapperClassName:t.wrapperClassName;var u=e("<div></div>").attr("id",s+"-sticky-wrapper").addClass(r.wrapperClassName);n.wrapAll(u);if(r.center){n.parent().css({width:n.outerWidth(),marginLeft:"auto",marginRight:"auto"})}if(n.css("float")=="right"){n.css({"float":"none"}).parent().css({"float":"right"})}var a=n.parent();a.css("height",n.outerHeight());i.push({topSpacing:r.topSpacing,bottomSpacing:r.bottomSpacing,stickyElement:n,currentTop:null,stickyWrapper:a,className:r.className,getWidthFrom:r.getWidthFrom,responsiveWidth:r.responsiveWidth})})},update:o,unstick:function(t){return this.each(function(){var t=e(this);var n=-1;for(var r=0;r<i.length;r++){if(i[r].stickyElement.get(0)==t.get(0)){n=r}}if(n!=-1){i.splice(n,1);t.unwrap();t.removeAttr("style")}})}};if(window.addEventListener){window.addEventListener("scroll",o,false);window.addEventListener("resize",u,false)}else if(window.attachEvent){window.attachEvent("onscroll",o);window.attachEvent("onresize",u)}e.fn.sticky=function(t){if(a[t]){return a[t].apply(this,Array.prototype.slice.call(arguments,1))}else if(typeof t==="object"||!t){return a.init.apply(this,arguments)}else{e.error("Method "+t+" does not exist on jQuery.sticky")}};e.fn.unstick=function(t){if(a[t]){return a[t].apply(this,Array.prototype.slice.call(arguments,1))}else if(typeof t==="object"||!t){return a.unstick.apply(this,arguments)}else{e.error("Method "+t+" does not exist on jQuery.sticky")}};e(function(){setTimeout(o,0)})})(jQuery)
