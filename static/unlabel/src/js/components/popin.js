import tabbable from 'tabbable'

export default class Popin {
  constructor({el, options = {}}) {
    this.el = el
    this.id = this.el.getAttribute('id')

    if( !this.id && !options.openSelector ) {
      console.error(`[Popin] The popin root has no "id" attribute so the default option 'openSelector: a[href="#ELEMENT_ID"]' won't work. You can either provide a popin id or override the 'openSelector' option.`)
    }

    // default options
    this.options = {
      openSelector: `a[href="#${this.id}"]`,
      closeSelector: '.popin__close, .popin__overlay',
      preventBodyScroll: true
    }
    Object.keys(this.options).forEach((key) => {
      this.options[key] = (Object.keys(options).indexOf(key) > -1) ? options[key] : this.options[key]
    })

    this.is_visible = null

    this.bindMethods()
    this.init()
    this.addEvents()

    this.hide(true)
  }
  bindMethods() {
    this.onClickOpen = this.onClickOpen.bind(this)
    this.onClickClose = this.onClickClose.bind(this)
    this.onKeyDown = this.onKeyDown.bind(this)
    this.shown = this.shown.bind(this)
    this.hidden = this.hidden.bind(this)
  }
  init(){
    this.open_btns_arr = [].slice.call(document.querySelectorAll(this.options.openSelector))
    if( this.open_btns_arr.length == 0 ){
      console.error(`[Popin] Can't find any elements to open the popin. Current 'openSelector' option is : ${this.options.openSelector}`)
    }
    this.close_btns_arr = [].slice.call(this.el.querySelectorAll(this.options.closeSelector))
    if( this.close_btns_arr.length == 0 ){
      console.error(`[Popin] Can't find any elements to close the popin. Current 'closeSelector' option is : ${this.options.closeSelector}`)
    }
  }
  addEvents() {
    // Open btns
    this.open_btns_arr.forEach((btn_el) => {
      btn_el.addEventListener('click', this.onClickOpen)
    })
      
    // Close btns
    this.close_btns_arr.forEach((btn_el) => {
      btn_el.addEventListener('click', this.onClickClose)
    })
  }
  beforeShow() {
    this.el.style.display = 'block'
    this.is_visible = true
    if( this.options.preventBodyScroll ){
      document.body.style.overflow = 'hidden'
    }
    window.addEventListener('keydown', this.onKeyDown)
    this.manageAccessibility(true)
  }
  show(prevent_anim = false){
    this.beforeShow()

    if( prevent_anim ){
      this.transitionIn(0)
    } else {
      this.transitionIn()
    }
  }
  transitionIn(speed = 0) {
    // Do your animation and then call this.after() when it's over
    this.shown()
  }
  shown() {
  }
  beforeHide() {

  }
  hide(prevent_anim = false){
    this.beforeHide()

    if( prevent_anim ){
      this.transitionOut(0)
    } else {
      this.transitionOut()
    }
  }
  transitionOut(speed = 0) {
    // Do your animation and then call this.hidden() when it's over
    this.hidden()
  }
  hidden() {
    window.removeEventListener('keydown', this.onKeyDown)
    if( this.options.preventBodyScroll ){
      document.body.style.overflow = ''
    }
    this.manageAccessibility(false)
    this.el.style.display = 'none'
    this.is_visible = false
  }
  onClickClose(e) {
    e.preventDefault()
    this.hide()
  }
  onClickOpen(e) {
    e.preventDefault()
    this.show()
  }
  onKeyDown(e) {
    switch( e.keyCode ) {
      case 27 : { // esc
        this.hide()
        break
      }
      case 9: { //tab
        // Keep focus on popin :
        // If last tabbable element is focused and the user press tab (whithout shift key),
        // then loop back to first tabbable element
        // Else If first tabbable element is focused and the user press tab (with shift key),
        // then loop forward to last tabbable element
        if( this.tabbable_el_arr && this.tabbable_el_arr.length > 0){
          if( this.tabbable_el_arr[this.tabbable_el_arr.length - 1] == document.activeElement && !e.shiftKey ){
            e.preventDefault()
            this.tabbable_el_arr[0].focus()
          } else if( this.tabbable_el_arr[0] == document.activeElement && e.shiftKey ){
            e.preventDefault()
            this.tabbable_el_arr[this.tabbable_el_arr.length - 1].focus()
          }
        }
        break
      }
    }
  }
  manageAccessibility(override = true) {
    if( override ){
      this.tabbable_el_arr = tabbable(this.el)
      this.el.setAttribute('aria-hidden', false)
      if( this.tabbable_el_arr.length > 0 ){
        this.tabbable_el_arr[0].focus()
      }
    }
    else {
      this.el.setAttribute('aria-hidden', true)
    }
  }
}