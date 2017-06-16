import Toggle from './toggle'

class SizeChart {
  constructor({el}) {    
    this.el = el

    this._unit = false

    this.bindMethods()
    this.init()
    this.addEvents()
  }
  // ----------------------------------------------------------------------------------------
  // Public methods
  // ----------------------------------------------------------------------------------------
  bindMethods() {
    this.handleToggleChanged = this.handleToggleChanged.bind(this)
  }
  init() {
    this.sizes_arr = [].slice.call(this.el.querySelectorAll('[data-sizechart-unit]'))

    // Toggle
    this.toggle_ctrl = new Toggle({
      el: this.el.querySelector('.toggle')
    })

    // Init State
    this.unit = this.toggle_ctrl.value
  }
  addEvents() {
    this.toggle_ctrl.on('changed', this.handleToggleChanged)
  }
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
  // ----------------------------------------------------------------------------------------
  // Getter/Setter methods
  // ----------------------------------------------------------------------------------------
  set unit(value) {
    this._unit = value
    this.updateUI()
  }
  get unit() {
    return this._unit
  }
}

module.exports = SizeChart