import zxcvbn from 'zxcvbn'

class PasswordSecurity {
  constructor({el}) {    
    this.el = el

    this._score = 0

    this.bindMethods()
    this.init()
    this.addEvents()
  }
  bindMethods(){
    this.onInputChanged = this.onInputChanged.bind(this)
  }
  init() {
    this.input_el = document.getElementById(this.el.getAttribute('data-password-security-id'))
    if( !this.input_el ){
      console.error('[PasswordSecurity] Couldn\'t find the input element to check. Use the attribute data-password-security-id to provide the input id.')
    }
  }
  addEvents() {
    this.input_el.addEventListener('input', this.onInputChanged)
    this.onInputChanged()
  }
  onInputChanged() {
    this.score = zxcvbn(this.input_el.value).score
    console.log('onInputChanged', this.score)
  }
  updateUI() {
    this.el.setAttribute('data-password-security-score', this.score)
  }
  get score() {
    return this._score
  }
  set score(value) {
    this._score = value

    this.updateUI()
  }
}

module.exports = PasswordSecurity