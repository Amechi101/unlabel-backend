import {TweenLite, Power3} from 'gsap'

class Collapsible {
  constructor({el, toggler_el, options = {}}) {    
    this.el = el
    this.toggler_el = toggler_el
    this.options = {
      collapsedClassname: 'is-collapsed',
      collapsedOnInit: true,
      collapseSpeed: 0.3,
      uncollapseSpeed: 0.3,
      collapseEase: Power3.easeOut,
      uncollapseEase: Power3.easeOut
    }
    this._collapsed = false

    Object.keys(this.options).forEach((key) => {
      this.options[key] = (Object.keys(options).indexOf(key) > -1) ? options[key] : this.options[key]
    })

    this.bindMethods()
    this.init()
    this.addEvents()
  }
  // ----------------------------------------------------------------------------------------
  // Public methods
  // ----------------------------------------------------------------------------------------
  bindMethods() {
    this.handleClickToggler = this.handleClickToggler.bind(this)
  }
  init() {
    if( this.options.collapsedOnInit ){
      this.collapse(true)
    }
  }
  addEvents() {
    this.toggler_el.addEventListener('click', this.handleClickToggler)
  }
  handleClickToggler(e) {
    e.preventDefault()
    e.stopImmediatePropagation()

    if( this._collapsed ){
      this.uncollapse()
    } else {
      this.collapse()
    }
  }
  uncollapse(prevent_anim = false) {
    let item_min_height = 0
    const children_arr = [].slice.call(this.el.children)
    children_arr.forEach((child_el) => {
      item_min_height += child_el.getBoundingClientRect().height
    })

    this._collapsed = false

    this.el.classList.remove(this.options.collapsedClassname)
    this.toggler_el.classList.remove(this.options.collapsedClassname)

    TweenLite.to(this.el, prevent_anim ? 0 : this.options.uncollapseSpeed, {maxHeight: item_min_height, clearProps: 'maxHeight', ease: this.options.uncollapseEase})
  }
  collapse(prevent_anim = false) {
    const current_height = this.el.getBoundingClientRect().height

    this._collapsed = true

    this.el.classList.add(this.options.collapsedClassname)
    this.toggler_el.classList.add(this.options.collapsedClassname)

    TweenLite.fromTo(this.el, prevent_anim ? 0 : this.options.collapseSpeed, {maxHeight: current_height + 'px'}, {maxHeight: 0, ease: this.options.collapseEase})
  }
  get isCollapsed() {
    return this._collapsed
  }
}

module.exports = Collapsible
