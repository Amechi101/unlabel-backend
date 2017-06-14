import {EventEmitter} from 'events'
import device from '../utils/device'

class Base extends EventEmitter {
  constructor({el, options = {}, default_options = {}}) {
    super(...arguments)
    
    this.el = el
    this.options = options

    this.settings = {}
    Object.keys(default_options).forEach((key) => {
      this.settings[key] = options[key] || default_options[key]
    })

    this.bindMethods()
    this.init()
    this.addEvents()
  }
  bindMethods(){
    this.onResize = this.onResize.bind(this)
    this.onDeviceChanged = this.onDeviceChanged.bind(this)
  }
  init() {
  }
  addEvents() {
    device.on('viewport_resized', this.onResize)
    device.on('device_changed', this.onDeviceChanged)
  }
  onResize() {
  }
  onDeviceChanged() {
  }
}

module.exports = Base