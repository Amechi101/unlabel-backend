import device from '../utils/device'
import ScrollMagic from 'scrollmagic'
// import {} from 'scrollmagic/scrollmagic/uncompressed/plugins/debug.addindicators.js' // for debugging

class AnchorsNav {
  constructor({el}) {    
    this.el = el

    this.parent_el = this.el.parentElement
    this.scroll_ctrl = new ScrollMagic.Controller()
    this.links_arr = [].slice.call(this.el.querySelectorAll('a[href^="#"]'))
    this.anchors_arr = [] 
    this.targets_arr = [] 
    this.targets_cachedHeights_arr = []

    this.bindMethods()
    this.init()
    this.addEvents()
  }
  bindMethods(){
    this.onResize = this.onResize.bind(this)
    this.onDeviceChanged = this.onDeviceChanged.bind(this)
  }
  init() {
    this.links_arr.forEach((el) => {
      const target_el = document.querySelector(el.getAttribute('href'))
      if( target_el ) {
        this.anchors_arr.push(el)
        this.targets_arr.push(target_el)
      }
    })

    this.cacheTargetsHeights()

    this.anchors_arr.forEach((el, index) => { 
      new ScrollMagic.Scene({
        triggerElement: this.targets_arr[index],
        duration: ()=> {
          return this.getContentHeightByIndex(index)
        }
      })
        .setClassToggle(el, 'is-active')
        // .addIndicators() // for debugging
        .addTo(this.scroll_ctrl)
    })

    new ScrollMagic.Scene({
      triggerElement: this.parent_el,
      triggerHook: 0
    })
      .setClassToggle(this.el, 'is-fixed')
      // .addIndicators() // for debugging
      .addTo(this.scroll_ctrl)
      .on('enter', () => {
        this.el.style.top = (this.el.offsetTop - this.parent_el.offsetTop) + 'px'
      })
      .on('leave', () => {
        this.el.style.top = ''
      })

    this.updateScrollController()
  }
  addEvents() {
    device.on('viewport_resized', this.onResize)
    device.on('device_changed', this.onDeviceChanged)
  }
  onResize() {
    this.cacheTargetsHeights()
    // this.updateUI()
  }
  onDeviceChanged() {
    this.updateScrollController()
  }
  /**
   * Cache targets heights in an array for fast computing during scroll
   * @return {array} Array of heights
   */
  cacheTargetsHeights() {
    this.anchors_arr.forEach((link_el, index) => {
      const target_el = document.querySelector(link_el.getAttribute('href'))
      const next_link_el = this.anchors_arr[index + 1] || false
      let height = 0
      // if not last element, get scroll difference between this target element and the next one
      // otherwise leave to 0 so scrollmagic interpret it as Infinite
      if( next_link_el ) { 
        const next_target_el = document.querySelector(next_link_el.getAttribute('href'))
        const target_offsetTop = target_el.getBoundingClientRect().top + (window.pageYOffset || document.documentElement.scrollTop)
        const next_target_offsetTop = next_target_el.getBoundingClientRect().top + (window.pageYOffset || document.documentElement.scrollTop)
        height = next_target_offsetTop - target_offsetTop
      }
      this.targets_cachedHeights_arr[index] = height
    })
  }
  /**
   * Get target height by index from cached array
   * @param  {int} index - target index in cached array
   * @return {int} target chached height
   */
  getContentHeightByIndex(index) {
    return this.targets_cachedHeights_arr[index]
  }
  updateScrollController() {
    this.scroll_ctrl.enabled(device.isMobile ? false : true)
    this.scroll_ctrl.update(true) // update immediatly
  }
}

module.exports = AnchorsNav