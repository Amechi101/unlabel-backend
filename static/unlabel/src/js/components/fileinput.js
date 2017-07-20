class FileInput {
  constructor({el, options = {}}) {
    this.el = el
    this.options = {
      multipleCaptionAttr : 'data-multiple-caption',
      multipleCountPlaceholderAttr : 'data-multiple-count-placeholder',
      inputSelector: '.fileinput__input',
      btnSelector: '.fileinput__btn',
      filenameSelector: '.fileinput__filename'
    }

    Object.keys(this.options).forEach((key) => {
      this.options[key] = (Object.keys(options).indexOf(key) > -1) ? options[key] : this.options[key]
    })

    this.bindMethods()
    this.init()
    this.addEvents()
  }
  bindMethods(){
    this.onRealInputChanged = this.onRealInputChanged.bind(this)
  }
  init() {
    this.real_input_el = this.el.querySelector( this.options.inputSelector )
    this.btn_el = this.el.querySelector( this.options.btnSelector )
    this.filename_el = this.el.querySelector( this.options.filenameSelector )
    this.default_filename = this.filename_el.innerHTML
    this.multiple_caption = this.el.getAttribute( this.options.multipleCaptionAttr ) || ''
    this.multiple_count_placeholder = this.el.getAttribute( this.options.multipleCountPlaceholderAttr ) || ''
  }
  addEvents() {
    this.real_input_el.addEventListener('change', this.onRealInputChanged)
  }
  onRealInputChanged() {
    let filename = null

    if( this.real_input_el.files && this.real_input_el.files.length > 1 ){
      if( this.multiple_count_placeholder ){
        filename = this.multiple_caption.replace(this.multiple_count_placeholder, this.real_input_el.files.length)
      } else {
        filename = this.multiple_caption
      }
    } else {
      filename = this.real_input_el.value.split( '\\' ).pop()
    }

    this.filename_el.innerHTML = filename || this.default_filename
  }
}

module.exports = FileInput