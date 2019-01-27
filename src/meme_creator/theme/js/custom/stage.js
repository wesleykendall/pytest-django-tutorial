import $ from 'jquery'
import Util from '../bootstrap/util'

/**
 * --------------------------------------------------------------------------
 * Bootstrap (v4.0.0): stage.js
 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
 * --------------------------------------------------------------------------
 */

const Stage = (($) => {

  /**
   * ------------------------------------------------------------------------
   * Constants
   * ------------------------------------------------------------------------
   */

  const NAME                = 'stage'
  const DATA_KEY            = 'bs.stage'
  const VERSION             = 'v4.0.0'
  const DATA_API            = '[data-toggle="stage"]'
  const EVENT_KEY           = `.${DATA_KEY}`
  const DATA_API_KEY        = '.data-api'
  const JQUERY_NO_CONFLICT  = $.fn[NAME]
  const TRANSITION_DURATION = 150

  const Default = {
    easing         : 'cubic-bezier(.2,.7,.5,1)',
    duration       : 300,
    delay          : 0,
    distance       : 250,
    hiddenElements : '#sidebar'
  }

  const Event = {
    TOUCHMOVE      : `touchmove${EVENT_KEY}`,
    KEYDOWN        : `keydown${EVENT_KEY}`,
    OPEN           : `open${EVENT_KEY}`,
    OPENED         : `opened${EVENT_KEY}`,
    CLOSE          : `close${EVENT_KEY}`,
    CLOSED         : `closed${EVENT_KEY}`,
    CLICK          : `click${EVENT_KEY}`,
    CLICK_DATA_API : `click${EVENT_KEY}${DATA_API_KEY}`
  }

  const ClassName = {
    STAGE_OPEN : 'stage-open',
    HIDDEN     : 'hidden'
  }


  /**
   * ------------------------------------------------------------------------
   * Class Definition
   * ------------------------------------------------------------------------
   */

   class Stage {

     constructor(element, config) {
       if (!Util.supportsTransitionEnd()) return

       this._element  = element
       this._config   = config
     }

     // getters

     static get VERSION() {
       return VERSION
     }

     static get Default() {
       return Default
     }

     // private

     _isOpen() {
       return $(this._element).hasClass(ClassName.STAGE_OPEN)
     }

     _complete() {
       $(document.body).css('overflow', 'auto')

       if ('ontouchstart' in document.documentElement) {
         $(document).off(Event.TOUCHMOVE)
       }

       $(this._config.hiddenElements).addClass(ClassName.HIDDEN)

       $(this._element)
         .removeClass(ClassName.STAGE_OPEN)
         .css({
           '-webkit-transition': '',
               '-ms-transition': '',
                   'transition': ''
         })
         .css({
           '-webkit-transform': '',
               '-ms-transform': '',
                   'transform': ''
         })
         .trigger(Event.CLOSED)
     }

     // public

     toggle() {
       if (this._isOpen()) {
         this.close()
       } else {
         this.open()
       }
     }

     open() {
       $(document.body).css('overflow', 'hidden')

       if ('ontouchstart' in document.documentElement) {
         $(document).on(Event.TOUCHMOVE, function (e) {
           e.preventDefault()
         })
       }

       $(this._config.hiddenElements).removeClass(ClassName.HIDDEN)

       $(window).one(Event.KEYDOWN, $.proxy(function (e) {
         e.which == 27 && this.close()
       }, this))

       $(this._element)
         .on(Event.CLICK, $.proxy(this.close, this))
         .trigger(Event.OPEN)
         .addClass(ClassName.STAGE_OPEN)

       if (!Util.supportsTransitionEnd()) {
         $(this._element)
           .css({
             'left': this._config.distance + 'px',
             'position': 'relative'
           })
           .trigger(Event.OPENED)
         return
       }

       $(this._element)
         .css({
           '-webkit-transition': '-webkit-transform ' + this._config.duration + 'ms ' + this._config.easing,
               '-ms-transition': '-ms-transform ' + this._config.duration + 'ms ' + this._config.easing,
                   'transition': 'transform ' + this._config.duration + 'ms ' + this._config.easing
         })

       this._element.offsetWidth // force reflow

       $(this._element)
         .css({
           '-webkit-transform': 'translateX(' + this._config.distance + 'px)',
               '-ms-transform': 'translateX(' + this._config.distance + 'px)',
                   'transform': 'translateX(' + this._config.distance + 'px)'
         })
         .one(Util.TRANSITION_END, () => {
           $(this._element).trigger(Event.OPENED)
         })
         .emulateTransitionEnd(this._config.duration)
     }

     close() {
       $(window).off(Event.KEYDOWN)

       if (!Util.supportsTransitionEnd()) {
         $(this._element)
           .trigger(Event.CLOSE)
           .css({ 'left': '', 'position': '' })
           .off(Event.CLICK)

         return this._complete()
       }

       $(this._element)
         .trigger(Event.CLOSE)
         .off(Event.CLICK)
         .css({
           '-webkit-transform': 'none',
               '-ms-transform': 'none',
                   'transform': 'none'
         })
         .one(Util.TRANSITION_END, $.proxy(this._complete, this))
         .emulateTransitionEnd(this._config.duration)
     }

     // static

     static _jQueryInterface(config) {
       return this.each(function () {
         var $this   = $(this)
         var data    = $this.data(DATA_KEY)
         var _config = $.extend(
           {},
           Default,
           $this.data(),
           typeof config === 'object' && config
         )

         if (!data) $this.data(DATA_KEY, (data = new Stage(this, _config)))
         if (typeof config === 'string') data[config]()
       })
     }
  }

  /**
   * ------------------------------------------------------------------------
   * jQuery
   * ------------------------------------------------------------------------
   */

  $.fn[NAME]             = Stage._jQueryInterface
  $.fn[NAME].Constructor = Stage
  $.fn[NAME].noConflict  = function () {
    $.fn[NAME] = JQUERY_NO_CONFLICT
    return Stage._jQueryInterface
  }

  /**
   * ------------------------------------------------------------------------
   * Data Api implementation
   * ------------------------------------------------------------------------
   */

  $(document).on(Event.CLICK_DATA_API, DATA_API, function () {
    var config  = $(this).data()
    var $target = $(this.getAttribute('data-target'))

    if (!$target.data(DATA_KEY)) {
     $target.stage(config)
    }

    $target.stage('toggle')
  })

  return Stage

})(jQuery)

export default Stage
