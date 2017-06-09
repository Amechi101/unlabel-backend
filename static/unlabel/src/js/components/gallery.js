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
    this.thumbs_links_arr = [].slice.call(this.thumbs_carousel_el.querySelectorAll('.gallery__link'))
    
    this.initThumbsCarousel()
    this.initPhotosCarousel()
    this.updateUI()
  }
  addEvents() {
    super.addEvents(...arguments)

    // Thumbs clicks
    this.thumbs_links_arr.forEach((link_el)=> {
      link_el.addEventListener('click', this.handleThumbClick)
    })
  }
  onDeviceChanged() {
    super.onResize(...arguments)
    this.reset()
  }
  // ----------------------------------------------------------------------------------------
  // Public methods
  // ----------------------------------------------------------------------------------------
  initThumbsCarousel() {
    if(this.thumbsCarousel) {
      this.thumbsCarousel.destroy(true, true)
    }
    this.thumbsCarousel = new Swiper(this.thumbs_carousel_el, {
      direction: device.isMobile ? 'horizontal' : 'vertical',
      // centeredSlides: true,
      slidesPerView: 'auto',
      touchRatio: 0.2,
      slideToClickedSlide: true
    })
  }
  initPhotosCarousel() {
    if(this.largesCarousel) {
      this.largesCarousel.destroy(true, true)
    }
    this.largesCarousel = new Swiper(this.larges_carousel_el, {
      slidesPerView: 1,
      onSlideChangeEnd: () => {
        this.updateUI()
      }
    })
  }
  handleThumbClick(e) {
    e.preventDefault()
    this.largesCarousel.slideTo(e.currentTarget.getAttribute('data-slide-to'))
    this.updateUI()
  }
  updateUI() {
    this.updateActiveThumb() 
  }
  updateActiveThumb() {
    this.thumbs_links_arr.forEach((link_el)=> {
      if(link_el.getAttribute('data-slide-to') == this.largesCarousel.realIndex) {
        link_el.classList.add('is-active')
      }
      else {
        link_el.classList.remove('is-active')
      }
    })
  }
  reset() {
    this.initThumbsCarousel()
    this.initPhotosCarousel()
    this.updateUI()
  }
}

module.exports = Gallery