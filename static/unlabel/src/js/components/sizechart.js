import Base from './_base'
import Toggle from './toggle'

class SizeChart extends Base {
  // ----------------------------------------------------------------------------------------
  // Overridden methods
  // ----------------------------------------------------------------------------------------
  bindMethods() {
    super.bindMethods(...arguments)

    this.handleToggleChanged = this.handleToggleChanged.bind(this)
  }
  init() {
    super.init(...arguments)

    this._unit = false

    this.sizes_arr = [].slice.call(this.el.querySelectorAll('[data-sizechart-unit]'))

    // Toggle
    this.toggle_ctrl = new Toggle({
      el: this.el.querySelector('.toggle')
    })

    // Init State
    this.unit = this.toggle_ctrl.value
  }
  addEvents() {
    super.addEvents(...arguments)

    this.toggle_ctrl.on('changed', this.handleToggleChanged)
  }
  // ----------------------------------------------------------------------------------------
  // Public methods
  // ----------------------------------------------------------------------------------------
  handleToggleChanged(value) {
    this.unit = value
  }
  updateUI() {
    this.sizes_arr.forEach((el) => {
      if( el.getAttribute('data-sizechart-unit') == this.unit ){
        el.style.display = ''
      }
      else {
        el.style.display = 'none'
      }
    })
  }
  set unit(value) {
    this._unit = value
    this.updateUI()
  }
  get unit() {
    return this._unit
  }
}

module.exports = SizeChart