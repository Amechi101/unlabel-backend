import Base from './_base'

class Toggle extends Base {
  // ----------------------------------------------------------------------------------------
  // Overridden methods
  // ----------------------------------------------------------------------------------------
  bindMethods() {
    super.bindMethods(...arguments)

    this.handleClickLabel = this.handleClickLabel.bind(this)
    this.handleClickSlider = this.handleClickSlider.bind(this)
  }
  init() {
    super.init(...arguments)

    this._value = false

    this.labels_arr = [].slice.call(this.el.querySelectorAll('[data-toggle-value]'))
    this.slider_el = this.el.querySelector('.toggle__slider')
    this.values_arr = this.slider_el.getAttribute('data-toggle-values').split(',')

    this.initSate()
  }
  addEvents() {
    super.addEvents(...arguments)

    this.labels_arr.forEach((label) => {
      label.addEventListener('click', this.handleClickLabel)  
    })

    this.slider_el.addEventListener('click', this.handleClickSlider)
  }
  // ----------------------------------------------------------------------------------------
  // Public methods
  // ----------------------------------------------------------------------------------------
  initSate() {
    let active_label = false
    // Get active label from dom
    this.labels_arr.forEach((label) => {
      if( label.classList.contains('is-active') ){
        active_label = label
      }
    })

    // If no active label, get first label element
    if( !active_label && this.labels_arr.length > 0 ){
      active_label = this.labels_arr[0]
    }

    if( active_label ){
      this.value = active_label.getAttribute('data-toggle-value')
    }
  }
  handleClickLabel(e) {
    e.preventDefault()
    this.value = e.currentTarget.getAttribute('data-toggle-value')
  }
  handleClickSlider(e) {
    e.preventDefault()
    this.value = this._value == this.values_arr[0] ? this.values_arr[1] : this.values_arr[0]
  }
  updateUI() {
    this.updateActiveLabel()
    this.updateSliderPos()
  }
  updateActiveLabel() {
    this.labels_arr.forEach((label) => {
      const label_value = label.getAttribute('data-toggle-value')
      if(label_value == this._value) {
        label.classList.add('is-active')
      } else {
        label.classList.remove('is-active')
      }
    })
  }
  updateSliderPos() {
    this.slider_el.classList.remove('is-left')
    this.slider_el.classList.remove('is-right')

    if( this.values_arr[0] == this._value ){
      this.slider_el.classList.add('is-left')
    } else if( this.values_arr[1] == this._value ){
      this.slider_el.classList.add('is-right')
    }
  }
  set value(value){
    const changed = this._value != value
    this._value = value
    this.updateUI()
    if( changed ){
      this.emit('changed', this._value)
    }
  }
  get value(){
    return this._value
  }
}

module.exports = Toggle