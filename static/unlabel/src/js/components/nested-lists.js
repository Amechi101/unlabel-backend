import {TweenLite, Power3} from 'gsap'
import closest from 'closest'

class NestedLists {
  constructor({el, options = {}}) {    
    this.el = el
    this.options = {
      itemsSelector: '.nested-lists__item',
      linksSelector: '.nested-lists__link',
      sublistSelector: '.nested-lists__list',
      openClassname: 'is-open' 
    }

    Object.keys(this.options).forEach((key) => {
      this.options[key] = options[key] || this.options[key]
    })

    this.bindMethods()
    this.init()
    this.addEvents()
  }
  // ----------------------------------------------------------------------------------------
  // Public methods
  // ----------------------------------------------------------------------------------------
  bindMethods() {
    this.handleClickLink = this.handleClickLink.bind(this)
  }
  init() {
    this.links_arr = [].slice.call(this.el.querySelectorAll(this.options.linksSelector))
  }
  addEvents() {
    this.links_arr.forEach((link_el) => {
      const parent_item_el = closest(link_el, this.options.itemsSelector)
      const has_nested_list = !! parent_item_el.querySelector(this.options.sublistSelector)
      if( has_nested_list ){
        link_el.addEventListener('click', this.handleClickLink)
      }
    })
  }
  handleClickLink(e) {
    const link_el = e.currentTarget
    const parent_item_el = closest(link_el, this.options.itemsSelector)
    const nested_list = parent_item_el.querySelector(this.options.sublistSelector)

    if( nested_list ){
      e.preventDefault()
      e.stopImmediatePropagation()
      if( ! parent_item_el.classList.contains(this.options.openClassname) ){
        let item_min_height = 0
        const children_arr = [].slice.call(nested_list.children)
        children_arr.forEach((child_el) => {
          item_min_height += child_el.getBoundingClientRect().height
        })
        TweenLite.to(nested_list, 0.3, {minHeight: item_min_height, clearProps: 'minHeight', ease: Power3.easeOut, onComplete: ()=> {
          parent_item_el.classList.add(this.options.openClassname)
        }})
      }
      else {
        TweenLite.to(nested_list, 0.3, {height: 0, clearProps: 'height', ease: Power3.easeOut, onComplete: ()=> {
          parent_item_el.classList.remove(this.options.openClassname)
        }})
      }
    }
  }
}

module.exports = NestedLists
