import Base from './_base'
import Swiper from 'swiper'
import device from '../utils/device'

class Gallery extends Base {
  // ----------------------------------------------------------------------------------------
  // Overridden methods
  // ----------------------------------------------------------------------------------------
  bindMethods() {
    super.bindMethods(...arguments)

    this.handleThumbClick = this.handleThumbClick.bind(this)
  }
  init() {
    super.init(...arguments)

    this.larges_carousel_el = this.el.querySelector('.gallery__larges')
    this.thumbs_carousel_el = this.el.querySelector('.gallery__thumbs')
    this.has_thumbs_carousel = !! this.thumbs_carousel_el
    if( this.has_thumbs_carousel ){
      this.thumbs_links_arr = [].slice.call(this.thumbs_carousel_el.querySelectorAll('.gallery__link'))
    }
    
    this.initThumbsCarousel()
    this.initPhotosCarousel()
    this.updateUI()
  }
  addEvents() {
    super.addEvents(...arguments)

    if( this.has_thumbs_carousel ){
      // Thumbs clicks
      this.thumbs_links_arr.forEach((link_el)=> {
        link_el.addEventListener('click', this.handleThumbClick)
      })
    }
  }
  onDeviceChanged() {
    super.onDeviceChanged(...arguments)
    this.reset()
  }
  // ----------------------------------------------------------------------------------------
  // Public methods
  // ----------------------------------------------------------------------------------------
  initThumbsCarousel() {
    if( this.has_thumbs_carousel ){
      if(this.thumbs_carousel_ctrl) {
        this.thumbs_carousel_ctrl.destroy(true, true)
      }
      this.thumbs_carousel_ctrl = new Swiper(this.thumbs_carousel_el, {
        direction: device.isMobile ? 'horizontal' : 'vertical',
        // centeredSlides: true,
        slidesPerView: 'auto',
        touchRatio: 0.2,
        slideToClickedSlide: true
      })
    }
  }
  initPhotosCarousel() {
    console.log('initPhotosCarousel')
    if(this.larges_carousel_ctlr) {
      this.larges_carousel_ctlr.destroy(true, true)
    }
    this.larges_carousel_ctlr = new Swiper(this.larges_carousel_el, {
      slidesPerView: 'auto',
      onSlideChangeEnd: () => {
        this.updateUI()
      }
    })
  }
  handleThumbClick(e) {
    e.preventDefault()
    this.larges_carousel_ctlr.slideTo(e.currentTarget.getAttribute('data-slide-to'))
    this.updateUI()
  }
  updateUI() {
    this.updateActiveThumb() 
  }
  updateActiveThumb() {
    if( this.has_thumbs_carousel ){
      this.thumbs_links_arr.forEach((link_el)=> {
        if(link_el.getAttribute('data-slide-to') == this.larges_carousel_ctlr.realIndex) {
          link_el.classList.add('is-active')
        }
        else {
          link_el.classList.remove('is-active')
        }
      })
    }
  }
  reset() {
    this.initThumbsCarousel()
    this.initPhotosCarousel()
    this.updateUI()
  }
}

module.exports = Gallery