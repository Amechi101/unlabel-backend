import Base from './_base'
import {TweenLite, Power3} from 'gsap'

/**
 * TODO : define better behaviour
 * Allow user to toggle (open/close) sublists
 * Still allow the user to click on each link !
 * Maybe based items selector on link instead of parent item and use closest to retrieve the parent ?
 */

class NestedLists extends Base {
  constructor(props) {
    props.default_options = {
      itemsSelector: '.nested-lists__item',
      sublistSelector: '.nested-lists__list',
      openClassname: 'is-open' 
    }
    super(props)
  }
  // ----------------------------------------------------------------------------------------
  // Overridden methods
  // ----------------------------------------------------------------------------------------
  bindMethods() {
    super.bindMethods(...arguments)

    this.handleClickItem = this.handleClickItem.bind(this)
  }
  init() {
    super.init(...arguments)

    this.items_arr = [].slice.call(this.el.querySelectorAll(this.settings.itemsSelector))
  }
  addEvents() {
    super.addEvents(...arguments)

    this.items_arr.forEach((item_el) => {
      const has_nested_list = !! item_el.querySelector(this.settings.sublistSelector)
      if( has_nested_list ){
        item_el.addEventListener('click', this.handleClickItem)
      }
    })
  }
  // ----------------------------------------------------------------------------------------
  // Public methods
  // ----------------------------------------------------------------------------------------
  handleClickItem(e) {
    const item_el = e.currentTarget
    const nested_list = item_el.querySelector(this.settings.sublistSelector)

    if( nested_list ){
      e.preventDefault()
      e.stopImmediatePropagation()
      if( ! item_el.classList.contains(this.settings.openClassname) ){
        let item_min_height = 0
        const children_arr = [].slice.call(nested_list.children)
        children_arr.forEach((child_el) => {
          item_min_height += child_el.getBoundingClientRect().height
        })
        TweenLite.to(nested_list, 0.3, {minHeight: item_min_height, clearProps: 'minHeight', ease: Power3.easeOut, onComplete: ()=> {
          item_el.classList.add(this.settings.openClassname)
        }})
      }
      else {
        TweenLite.to(nested_list, 0.3, {height: 0, clearProps: 'height', ease: Power3.easeOut, onComplete: ()=> {
          item_el.classList.remove(this.settings.openClassname)
        }})
      }
    }
  }
}

module.exports = NestedLists
