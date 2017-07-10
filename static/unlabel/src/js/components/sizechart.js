import Toggle from './toggle'

class SizeChart {
  constructor({el}) {    
    this.el = el

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
    this.toggles_el_arr = [].slice.call(this.el.querySelectorAll('.toggle'))
    this.toogles_ctrl_arr = []

    // Toggles
    this.toggles_el_arr.forEach((toggle_el) => {
      this.toogles_ctrl_arr.push(new Toggle({
        el: toggle_el
      }))
    })

    // Init State
    this.toogles_ctrl_arr.forEach((toggle_ctrl) => {
      this.updateSizes(toggle_ctrl.value, toggle_ctrl.values_arr)
    })
  }
  addEvents() {
    this.toogles_ctrl_arr.forEach((toggle_ctrl) => {
      toggle_ctrl.on('changed', this.handleToggleChanged)
    })
  }
  handleToggleChanged(current_value, values_arr) {
    this.updateSizes(current_value, values_arr)
  }
  updateSizes(current_unit, units_arr) {
    this.sizes_arr.forEach((el) => {
      const el_unit = el.getAttribute('data-sizechart-unit')
      if( units_arr.indexOf(el_unit) > -1 ) {
        if( el_unit == current_unit ){
          el.style.display = ''
        }
        else {
          el.style.display = 'none'
        }
      }
    })
  }
}

module.exports = SizeChart