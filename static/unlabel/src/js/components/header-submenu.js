import device from '../utils/device'
import TweenLite from 'gsap'

class HeaderSubmenu {
  constructor({el, options = {}}) {
    this.el = el
    this.options = {}

    Object.keys(this.options).forEach((key) => {
      this.options[key] = (Object.keys(options).indexOf(key) > -1) ? options[key] : this.options[key]
    })

    this.bindMethods()
    this.init()
    this.addEvents()
  }
  bindMethods(){
    this.onResize = this.onResize.bind(this)
    this.onDeviceChanged = this.onDeviceChanged.bind(this)
    this.onMouseoverToggler = this.onMouseoverToggler.bind(this)
    this.onMouseoutToggler = this.onMouseoutToggler.bind(this)
    this.onClickTogglerLink = this.onClickTogglerLink.bind(this)
  }
  init() {
    this.toggler_el = this.el.parentElement
    this.toggler_link_el = this.toggler_el.querySelector('.header_linkWithSubmenu')
    this.contentWrapper_el = this.el.querySelector('.header__submenuWrapper')
    this.headerOverlay_el = document.querySelector('#header-submenu-overlay')

    this.hide(true)
    this.stickToright()
  }
  addEvents() {
    device.on('viewport_resized', this.onResize)
    device.on('device_changed', this.onDeviceChanged)

    this.toggler_link_el.addEventListener('click', this.onClickTogglerLink)
    this.toggler_el.addEventListener('mouseenter', this.onMouseoverToggler)
    this.toggler_el.addEventListener('mouseleave', this.onMouseoutToggler)
  }
  onResize() {
    this.hide(true)
  }
  onDeviceChanged() {
    this.hide(true)
  }
  onClickTogglerLink(e) {
    // Prevent click on all device except mobile
    if( !device.isMobile ){
      e.preventDefault()
    }
  }
  onMouseoverToggler() {
    if( !device.isMobile ){
      this.stickToright()
      this.show()
      this.toggler_el.classList.add('is-active')
    }
  }
  onMouseoutToggler() {
    this.hide()
    this.toggler_el.classList.remove('is-active')
  }
  killCurrentAnimation() {
    TweenLite.killTweensOf(this.headerOverlay_el)
    TweenLite.killTweensOf(this.el)
    TweenLite.killTweensOf(this.contentWrapper_el)
  }
  show(preventAnim = false) {
    this.killCurrentAnimation()
    TweenLite.to(this.headerOverlay_el, preventAnim ? 0 : 0.3, {'autoAlpha': 1})
    TweenLite.to(this.el, preventAnim ? 0 : 0.3, {'autoAlpha': 1})
    TweenLite.to(this.contentWrapper_el, preventAnim ? 0 : 0.3, {y:'0px'})
  }
  hide(preventAnim = false) {
    this.killCurrentAnimation()
    TweenLite.to(this.headerOverlay_el, preventAnim ? 0 : 0.2, {'autoAlpha': 0, delay: 0.05})
    TweenLite.to(this.el, preventAnim ? 0 : 0.2, {'autoAlpha': 0})
    TweenLite.to(this.contentWrapper_el, preventAnim ? 0 : 0.2, {y:'-20px'})
  }
  stickToright() {
    const toggler_clientRect = this.toggler_el.getBoundingClientRect()
    const translate_x = window.innerWidth - toggler_clientRect.left - toggler_clientRect.width 
    TweenLite.to(this.el, 0, {'x': `${translate_x}px`})
  }
}

module.exports = HeaderSubmenu