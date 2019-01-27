import $ from 'jquery'
import Util from '../bootstrap/util'

/**
 * --------------------------------------------------------------------------
 * Bootstrap (v4.0.0): enter.js
 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
 * --------------------------------------------------------------------------
 */

const Enter = (($) => {

  /**
   * ------------------------------------------------------------------------
   * Constants
   * ------------------------------------------------------------------------
   */

  const NAME                = 'enter'
  const DATA_KEY            = 'bs.enter'
  const VERSION             = 'v4.0.0'
  const DATA_API            = '[data-transition="entrance"]'
  const EVENT_KEY           = `.${DATA_KEY}`
  const DATA_API_KEY        = '.data-api'
  const JQUERY_NO_CONFLICT  = $.fn[NAME]

  const Event = {
    SCROLL : `scroll${EVENT_KEY}`,
    ENTER  : `enter${EVENT_KEY}`
  }

  const Default = {
    easing: 'cubic-bezier(.2,.7,.5,1)',
    duration: 1200,
    delay: 0
  }


  /**
   * ------------------------------------------------------------------------
   * Class Definition
   * ------------------------------------------------------------------------
   */

  class Enter {

    constructor(element, config) {
      if (!Util.supportsTransitionEnd()) return

      this._element  = element
      this._config   = config
      this._handler  = null
      this._listener = null

      this._addEventListeners()
    }

    // getters

    static get VERSION() {
      return VERSION
    }

    static get Default() {
      return Default
    }

    // public

    dispose() {
      $(this._element).off(EVENT_KEY)
      $.removeData(this._element, DATA_KEY)

      this._element  = null
      this._config   = null
      this._handler  = null
      this._listener = null
    }

    // private

    _addEventListeners() {
      const boundScrollHandler = $.proxy(this._checkForEnter, this)
      this._handler = function () { window.requestAnimationFrame(boundScrollHandler) }
      this._listener = $(window).on(Event.SCROLL, this._handler)
      this._checkForEnter()
    }

    _removeEventListeners() {
      $(window).off(Event.SCROLL, this._handler)
    }

    _checkForEnter() {
      const windowHeight  = window.innerHeight
      const rect          = this._element.getBoundingClientRect()

      if ((windowHeight - rect.top) >= 0) {
        setTimeout($.proxy(this._triggerEntrance, this), this._config.delay)
      }
    }

    _triggerEntrance() {
      this._removeEventListeners()

      $(this._element)
        .css({'-webkit-transition': '-webkit-transform ' + this._config.duration + 'ms ' + this._config.easing,
                  '-ms-transition': '-ms-transform ' + this._config.duration + 'ms ' + this._config.easing,
                      'transition': 'transform ' + this._config.duration + 'ms ' + this._config.easing
        })
        .css({'-webkit-transform': 'none',
                  '-ms-transform': 'none',
                      'transform': 'none'
         })
        .trigger(Event.ENTER)
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
          typeof config == 'object' && config
        )

        if (!data) $this.data(DATA_KEY, (data = new Enter(this, _config)))
        if (typeof config == 'string') data[config]()
      })
    }
  }

  /**
   * ------------------------------------------------------------------------
   * jQuery
   * ------------------------------------------------------------------------
   */

  $.fn[NAME]             = Enter._jQueryInterface
  $.fn[NAME].Constructor = Enter
  $.fn[NAME].noConflict  = function () {
    $.fn[NAME] = JQUERY_NO_CONFLICT
    return Enter._jQueryInterface
  }

  /**
   * ------------------------------------------------------------------------
   * Data Api implementation
   * ------------------------------------------------------------------------
   */

  $(function () {
   $(DATA_API).enter()
  })

  return Enter

})(jQuery)

export default Enter
