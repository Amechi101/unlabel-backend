import {TweenLite, Power3} from 'gsap'
import closest from 'closest'
import Collapsible from './collapsible'

class NestedLists {
  constructor({el, options = {}}) {    
    this.el = el
    this.options = {
      listSelector: '.nested-lists__list',
      togglerSelector: '.nested-lists__link',
      related: false // TODO : add behavior
    }

    Object.keys(this.options).forEach((key) => {
      this.options[key] = options[key] || this.options[key]
    })

    this.init()
  }
  // ----------------------------------------------------------------------------------------
  // Public methods
  // ----------------------------------------------------------------------------------------
  init() {
    this.lists_arr = [].slice.call(this.el.querySelectorAll(this.options.listSelector))

    this.lists_arr.forEach((list_el) => {
      const nested_list = list_el.querySelector(this.options.listSelector)
      if( nested_list ){
        const nested_list_toggler = list_el.querySelector(this.options.togglerSelector)
        const collapsible_ctrl = new Collapsible({
          el: nested_list,
          toggler_el: nested_list_toggler
        })
      }
    })
  }
}

module.exports = NestedLists
