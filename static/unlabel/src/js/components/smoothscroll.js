import {TweenLite} from 'gsap'
import ScrollToPlugin from 'gsap/ScrollToPlugin'

class Smoothscroll {
  constructor({el, options = {}}) {    
    this.el = el

    this.options = {
      offsetTop: 0 // offset from windows top
    }

    Object.keys(this.options).forEach((key) => {
      this.options[key] = options[key] || this.options[key]
    })

    this.target_selector = this.el.getAttribute('href')
    this.target_el = document.querySelector(this.target_selector)

    if( this.target_el ){
      this.bindMethods()
      this.addEvents()
    }
  }
  bindMethods(){
    this.onClick = this.onClick.bind(this)
  }
  addEvents() {
    this.el.addEventListener('click', this.onClick)
  }
  onClick(e) {
    e.preventDefault()
    TweenLite.to(window, 0.3, {scrollTo: this.target_el.offsetTop - this.options.offsetTop})
  }
}

module.exports = Smoothscroll