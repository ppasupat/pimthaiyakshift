$(function () {
  'use strict';

  const SCREEN_WIDTH = 700, SCREEN_HEIGHT = 400;
  const FRAME_RATE = 8;
  const SHIFT_CHARS = /[%+๑๒๓๔ู฿๕๖๗๘๙๐"ฎฑธํณ๊ฯญฐ,ฅฤฆฏโฌ็ษ๋ศซ.()ฉฮฺฒ์?ฬฦ]/g;

  let WORD_LIST;

  // ################################
  // Utilities

  function gup(name) {
    let regex = new RegExp("[\\?&]" + name + "=([^&#]*)");
    let results = regex.exec(window.location.href);
    return results === null ? "" : decodeURIComponent(results[1]);
  }

  function countShift(word) {
    return (word.match(SHIFT_CHARS) || []).length;
  }

  function showScene(name, callback) {
    $('.scene').hide();
    $('#scene-' + name).show();
    if (callback !== void 0) callback();
  }

  function showCover(name, delay, callback) {
    $('#cover-' + name).show();
    setTimeout(function () {
      $('#cover-' + name).hide();
      if (callback !== void 0) callback();
    }, delay);
  }

  // ################################
  // Menu

  function setupMenu() {
    showScene('menu');
  }

  $('#start-button').click(function () {

  });

	// ################################
  // Preloading and screen resizing

  function resizeScreen() {
    let ratio = Math.min(
      1.0,
      window.innerWidth / SCREEN_WIDTH,
      (window.innerHeight - 25) / SCREEN_HEIGHT,
    );
    $('#game-wrapper').css({
      'width': (SCREEN_WIDTH * ratio) + 'px',
      'height': (SCREEN_HEIGHT * ratio) + 'px',
    });
    $('#game').css('transform', 'scale(' + ratio + ')');
  }

  let numResourcesLeft = 1;

  function decrementPreload (kidding) {
    if (kidding !== 'kidding') numResourcesLeft--;
    if (numResourcesLeft === 0) {
      setupMenu();
    } else {
      $('#pane-loading').text('Loading resources (' + numResourcesLeft + ' left)');
    }
  }
  decrementPreload('kidding');

  $.getJSON('data/words.json', function (data) {
    WORD_LIST = data;
    decrementPreload();
  });

  resizeScreen();
  $(window).resize(resizeScreen);
  showScene('preload');

});
