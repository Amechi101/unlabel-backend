import Swiper from 'swiper'
import device from '../utils/device'
import {TweenMax} from 'gsap'

class Carousel {
  constructor({el}) {    
    this.el = el

    this.btn_prev_el = this.el.querySelector('.carousel__btn--prev')
    this.btn_next_el = this.el.querySelector('.carousel__btn--next')
    this.visuals_slider_el = this.el.querySelector('.carousel_visualsSlider')
    this.visuals_slider_ctrl = null
    this.contents_slider_el = this.el.querySelector('.carousel_contentsSlider')
    this.contents_slider_ctrl = null
    this.bg_slider_el = this.el.querySelector('.carousel__backgroundsSlider')
    this.bg_slider_ctrl = null

    this.bindMethods()
    this.init()
    this.addEvents()
  }
  // ----------------------------------------------------------------------------------------
  // Public methods
  // ----------------------------------------------------------------------------------------
  bindMethods() {
    this.onDeviceChanged = this.onDeviceChanged.bind(this)
    this.onSlideChanged = this.onSlideChanged.bind(this)
    this.onMouseEnter = this.onMouseEnter.bind(this)
    this.onMouseLeave = this.onMouseLeave.bind(this)
  }
  init() {
    this.initVisualsSlider()
    this.initContentsSlider()
    this.initBackgroundsSlider()
  }
  addEvents() {
    device.on('device_changed', this.onDeviceChanged)

    this.el.addEventListener('mouseenter', this.onMouseEnter)
    this.el.addEventListener('mouseleave', this.onMouseLeave)
  }
  onDeviceChanged() {
    this.reset()
  }
  initVisualsSlider() {
    if(this.visuals_slider_ctrl) {
      this.visuals_slider_ctrl.destroy(true, true)
    }
    this.visuals_slider_ctrl = new Swiper(this.visuals_slider_el, {
      prevButton: this.btn_prev_el,
      nextButton: this.btn_next_el,
      onSlideChangeStart: this.onSlideChanged,
      runCallbacksOnInit: true
    })
    this.visuals_slider_ctrl.disableKeyboardControl()
  }
  initContentsSlider() {
    if(this.contents_slider_ctrl) {
      this.contents_slider_ctrl.destroy(true, true)
    }
    this.contents_slider_ctrl = new Swiper(this.contents_slider_el, {
      onlyExternal: true,
      // virtualTranslate: true
      effect: 'fade',
      onTransitionStart: (swiper) => {
        const prev_children = [].slice.call(swiper.slides[swiper.previousIndex].children)
        const next_children = [].slice.call(swiper.slides[swiper.activeIndex].children)
        const is_reverse = swiper.activeIndex < swiper.previousIndex
        const prev_anim_speed = 0.2
        const prev_anim_delay = 0.05
        const prev_params_to = {
          y: is_reverse ? '20px' : '-20px',
          opacity: 0
        }
        const next_params_from = {
          y: is_reverse ? '-20px' : '20px',
          opacity: 0
        }
        const next_params_to = {
          y: '0%',
          opacity: 1,
          delay: (prev_anim_speed + prev_anim_delay * prev_children.length)
        }

        if( is_reverse ){
          prev_children.reverse()
          next_children.reverse()
        }
        
        TweenMax.killTweensOf(prev_children)
        TweenMax.killTweensOf(next_children)
        TweenMax.staggerTo(prev_children, prev_anim_speed, prev_params_to, prev_anim_delay)
        TweenMax.staggerFromTo(next_children, 0.5, next_params_from, next_params_to, 0.1)
      }
    })
  }
  initBackgroundsSlider() {
    if(this.bg_slider_ctrl) {
      this.bg_slider_ctrl.destroy(true, true)
    }
    this.bg_slider_ctrl = new Swiper(this.bg_slider_el, {
      effect: 'fade',
      onlyExternal: true
    })
  }
  onSlideChanged() {
    if( this.contents_slider_ctrl ){
      this.contents_slider_ctrl.slideTo(this.visuals_slider_ctrl.realIndex)
    }
    if( this.bg_slider_ctrl ){
      this.bg_slider_ctrl.slideTo(this.visuals_slider_ctrl.realIndex)
    }
  }
  onMouseEnter() {
    if( this.visuals_slider_ctrl ){
      this.visuals_slider_ctrl.enableKeyboardControl()
    }
  }
  onMouseLeave() {
    if( this.visuals_slider_ctrl ){
      this.visuals_slider_ctrl.disableKeyboardControl()
    }
  }
  reset() {
    this.initVisualsSlider()
    this.initContentsSlider()
    this.initBackgroundsSlider()
  }
}

module.exports = Carousel