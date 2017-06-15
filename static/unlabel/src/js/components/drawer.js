import Popin from './popin'
import device from '../utils/device'
import {TweenLite, Power3} from 'gsap'

class Drawer extends Popin {
  // ----------------------------------------------------------------------------------------
  // Overridden methods
  // ----------------------------------------------------------------------------------------
  bindMethods() {
    super.bindMethods(...arguments)
    this.onDeviceChanged = this.onDeviceChanged.bind(this)
  }
  init() {
    super.init(...arguments)

    this.backdrop_el = this.el.querySelector('.drawer__backdrop')
    this.frame_el = this.el.querySelector('.drawer__frame')
    this.scroller_el = this.el.querySelector('.drawer__scroller')
  }
  addEvents() {
    super.addEvents(...arguments)
    device.on('device_changed', this.onDeviceChanged)
  }
  beforeShow() {
    super.beforeShow(...arguments)
    this.scroller_el.scrollTop = 0 // scroller back to top
  }
  transitionIn(speed = 0.5) {
    TweenLite.to(this.backdrop_el, speed, {opacity: 0.7, ease: Power3.easeOut})
    TweenLite.to(this.frame_el, speed, {x: '0%', opacity: 1, onComplete: this.shown, ease: Power3.easeOut})
  }
  transitionOut(speed = 0.3) {
    TweenLite.to(this.backdrop_el, speed, {opacity: 0, ease: Power3.easeIn})
    TweenLite.to(this.frame_el, speed, {x: '50%', opacity: 0, onComplete: this.hidden, ease: Power3.easeIn})
  }
  // ----------------------------------------------------------------------------------------
  // Public methods
  // ----------------------------------------------------------------------------------------
  onDeviceChanged() {
    if( !device.isMobile && this.is_visible ) {
      this.hide(true)
    }
  }
}

module.exports = Drawer