$(function () {
  'use strict';

  const SCREEN_WIDTH = 700, SCREEN_HEIGHT = 400;
  const FRAME_RATE = 30;
  const TIME_LIMIT = 60000;
  const SHIFT_CHARS = /[%+๑๒๓๔ู฿๕๖๗๘๙๐"ฎฑธํณ๊ฯญฐ,ฅฤฆฏโฌ็ษ๋ศซ.()ฉฮฺฒ์?ฬฦ]/g;

  const WORD_LIST_URLS = [
    ['normal', 'data/words.json'],
  ], WORD_LISTS = {};
  let currentWordList = 'normal';

  // ################################
  // Utilities

  function gup(name) {
    let regex = new RegExp("[\\?&]" + name + "=([^&#]*)");
    let results = regex.exec(window.location.href);
    return results === null ? "" : decodeURIComponent(results[1]);
  }

  function showScene(name) {
    $('.scene').hide();
    $('#scene-' + name).show();
  }

  function showCover(name) {
    $('#cover-wrapper').show();
    $('.cover').hide();
    if (name) {
      $('#cover-' + name).show();
    }
  }

  function hideCover() {
    $('#cover-wrapper').hide();
  }

  function countShift(word) {
    return (word.match(SHIFT_CHARS) || []).length;
  }

  // ################################
  // Battle

  let timerHandler = null, timerStartTime = null, timerAmount = null;

  function startTimer(amountMs) {
    stopTimer();
    timerStartTime = Date.now();
    timerAmount = amountMs;
    timerHandler = window.setInterval(updateTimer, 1000. / FRAME_RATE);
    updateTimer();
  }

  function updateTimer() {
    let remaining = timerAmount - (Date.now() - timerStartTime);
    $('#hud-timer').text((remaining / 1000).toFixed(1));
    if (remaining <= 0) {
      stopTimer();
      setupSummary();
    } else {
      checkAnswer();
    }
  }

  function stopTimer() {
    if (timerHandler !== null) {
      window.clearInterval(timerHandler);
      timerHandler = null;
    }
  }

  let currentScore = 0, totalNumChars = 0, targetWord = null;

  function setupBattle() {
    currentScore = 0;
    totalNumChars = 0;
    nextQuestion();
    startTimer(TIME_LIMIT);
    showScene('battle');
    $('#answer-box').val('').focus();
  }

  function nextQuestion() {
    let targetIndex = Math.floor(
      Math.random() * WORD_LISTS[currentWordList].length);
    targetWord = WORD_LISTS[currentWordList][targetIndex];
    $('#target-word').text(targetWord);
    showScore();
  }

  function checkAnswer() {
    if ($('#answer-box').val() === targetWord) {
      currentScore += countShift(targetWord);
      totalNumChars += targetWord.length;
      nextQuestion();
      $('#answer-box').val('').focus();
    }
  }

  function showScore() {
    $('#hud-score').text(currentScore)
      .append('<span class=score-preview>' +
        ' + ' + countShift(targetWord) + '</span>');
  }

  // ################################
  // Summary

  function setupSummary() {
    $('#summary-pane').empty()
      .append('<p>คะแนน: ' + currentScore + '</p>')
      .append('<p class=summary-small>(หนึ่งคะแนนต่อ Shift)</p>')
      .append('<p>จำนวนอักขระรวม: ' + totalNumChars + '</p>');
    showScene('summary');
  }

  $('#back-button').click(setupMenu);

  // ################################
  // Menu

  function setupMenu() {
    showScene('menu');
  }

  function showCountdown() {
    showScene('countdown');
    let countdownCount = 4;
    function decrementCountdown() {
      countdownCount--;
      if (countdownCount === 0) {
        setupBattle();
      } else {
        $('#countdown-number').text(countdownCount);
        setTimeout(decrementCountdown, 500);
      }
    }
    decrementCountdown();
  }
  $('#start-button').click(showCountdown);

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

  let numResourcesLeft = WORD_LIST_URLS.length;

  function decrementPreload (kidding) {
    if (kidding !== 'kidding') numResourcesLeft--;
    if (numResourcesLeft === 0) {
      setupMenu();
    } else {
      $('#pane-loading').text('Loading resources (' + numResourcesLeft + ' left)');
    }
  }
  decrementPreload('kidding');

  WORD_LIST_URLS.forEach(function (entry) {
    $.getJSON(entry[1], function (data) {
      WORD_LISTS[entry[0]] = data;
      decrementPreload();
    });
  });

  resizeScreen();
  $(window).resize(resizeScreen);
  showScene('preload');

});
