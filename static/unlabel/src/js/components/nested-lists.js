import Base from './_base'

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
    const has_nested_list = item_el.querySelector(this.settings.sublistSelector)

    if( has_nested_list ){
      if( ! item_el.classList.contains(this.settings.openClassname) ){
        e.preventDefault()
        e.stopImmediatePropagation()
        item_el.classList.add(this.settings.openClassname)
      }
    }
  }
}

module.exports = NestedLists
