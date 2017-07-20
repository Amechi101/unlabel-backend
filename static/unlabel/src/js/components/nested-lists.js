import Collapsible from './collapsible'
import closest from 'closest'

class NestedLists {
  constructor({el, options = {}}) {    
    this.el = el
    this.options = {
      listSelector: '.nested-lists__list',
      parentSelector: '.nested-lists__item',
      togglerSelector: '.nested-lists__link'
    }

    Object.keys(this.options).forEach((key) => {
      this.options[key] = (Object.keys(options).indexOf(key) > -1) ? options[key] : this.options[key]
    })

    this.init()
  }
  // ----------------------------------------------------------------------------------------
  // Public methods
  // ----------------------------------------------------------------------------------------
  init() {
    this.lists_arr = [].slice.call(this.el.querySelectorAll(this.options.listSelector))

    this.lists_arr.forEach((list_el) => {
      const parent_el = closest(list_el, this.options.parentSelector)
      if( parent_el ){
        const list_toggler = parent_el.querySelector(this.options.togglerSelector)
        new Collapsible({
          el: list_el,
          toggler_el: list_toggler,
          options: {
            collapsedOnInit: list_toggler.classList.contains('is-active') ? false : true
          }
        })
      }
    })
  }
}

module.exports = NestedLists
