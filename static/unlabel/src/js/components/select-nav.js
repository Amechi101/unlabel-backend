class SelectNav {
  constructor({el}) {
    this.el = el

    this.bindMethods()
    this.addEvents()
  }
  bindMethods(){
    this.onChange = this.onChange.bind(this)
  }
  addEvents() {
    this.el.addEventListener('change', this.onChange)
  }
  onChange() {
    window.location = this.el.value
  }
}

module.exports = SelectNav