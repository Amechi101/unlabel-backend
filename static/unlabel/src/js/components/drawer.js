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

    this.anim_axis = this.el.classList.contains('drawer--top') ? 'y' : 'x'
    this.anim_direction = this.el.classList.contains('drawer--top') ? -1 : 1
  }
  addEvents() {
    super.addEvents(...arguments)
    device.on('device_changed', this.onDeviceChanged)
  }
  beforeShow() {
    super.beforeShow(...arguments)
    if( this.scroller_el ){
      this.scroller_el.scrollTop = 0 // scroller back to top
    }
  }
  transitionIn(speed = 0.5) {
    const frame_params = {
      [this.anim_axis]: '0%',
      opacity: 1,
      onComplete: this.shown,
      ease: Power3.easeOut
    }
    TweenLite.to(this.backdrop_el, speed, {opacity: 0.7, ease: Power3.easeOut})
    TweenLite.to(this.frame_el, speed, frame_params)
  }
  transitionOut(speed = 0.3) {
    const frame_params = {
      [this.anim_axis]: (50 * this.anim_direction) + '%',
      opacity: 0,
      onComplete: this.hidden,
      ease: Power3.easeIn
    }
    TweenLite.to(this.backdrop_el, speed, {opacity: 0, ease: Power3.easeIn})
    TweenLite.to(this.frame_el, speed, frame_params)
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