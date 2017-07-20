import {TweenLite} from 'gsap'
import ScrollToPlugin from 'gsap/ScrollToPlugin'

class Smoothscroll {
  constructor({el, options = {}}) {    
    this.el = el

    this.options = {
      offsetTop: 0 // offset from windows top
    }

    Object.keys(this.options).forEach((key) => {
      this.options[key] = (Object.keys(options).indexOf(key) > -1) ? options[key] : this.options[key]
    })

    this.bindMethods()
    this.addEvents()
  }
  bindMethods(){
    this.onClick = this.onClick.bind(this)
    this.onChange = this.onChange.bind(this)
  }
  addEvents() {
    if( this.el.nodeName == 'A' ) {
      this.el.addEventListener('click', this.onClick)
    }
    else if ( this.el.nodeName == 'SELECT' ) {
      this.el.addEventListener('change', this.onChange)
    }
  }
  onClick(e) {
    e.preventDefault()
    this.scrollTo(this.el.getAttribute('href'))
  }
  onChange() {
    this.scrollTo(this.el.value)
  }
  scrollTo(target_selector) {
    const target_el = document.querySelector(target_selector)

    if( target_el ){
      TweenLite.to(window, 0.3, {scrollTo: target_el.offsetTop - this.options.offsetTop})
    }
  }
}

module.exports = Smoothscroll