/*------------------------------------------------------------------
[Unlabel Main JS]

Copyright 2015, Unlabel
Website: https://www.unlabel.us
Email: info@unlabel.us
-------------------------------------------------------------------*/


var UnlabelModule = (function ( core, $ ) {

    /**
     * Private Methods
     */

    //http://coveroverflow.com/a/11381730/989439
    function mobilecheck() {
        var check = false;
        (function(a){if(/(android|ipad|playbook|silk|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0,4)))check = true})(navigator.userAgent||navigator.vendor||window.opera);
        return check;
    }

    //Check the event type for mobile or desktop
    var eventType =  mobilecheck() ? 'touchstart' : 'click';

    /**
     * Public API
     */

    core.utils = {
        scrollTopApi: function() {

            var elScroll = $('#scrollTop');
        
            $(window).scroll(function() {
                if( $(this).scrollTop() > 100 ) {
                    elScroll.fadeIn();

                } else {
                    elScroll.fadeOut();
                }
            });
            
            elScroll.on('click', function() {
                $('html, body').animate({
                    scrollTop:0
                }, 600);
                return false;
            });
        },
        scrollToSection:function() {
            $(document).ready(function() {
                var $win = $(window);
                
                $('.scroll-to-section').on('click', function(event) {
                    event.preventDefault();

                    var element = $(this).attr('href');
                    var scrollTo = $(element).offset().top;

                    $('body, html').animate({scrollTop: scrollTo}, Math.abs($win.scrollTop() - scrollTo) / 1.2);
                });
            });
        }
    },
    core.headerMenusToggleApi = {

        win: $(window),

        tween: false,

        menuToggle: false,

        filterToggle: false,

        init:function() {
            this.create();
            this.toggle();
        },
        create:function() {
            
            var _self = this;

            // menu navigation
            _self.panelTimeline = new TimelineMax({ 

                tweens:[
                
                    //Menu Container animation
                    TweenMax.to( _self.menu().menuContainer, .7, {x:'0%', force3D:true, ease:Cubic.easeInOut }) ,
                    
                    //Menu Items animation
                    new TimelineMax({ tweens:[
                        
                        TweenMax.allFrom( _self.menu().menuItems, .35, { x:'-100%', ease:Cubic.easeOut }, .06 ),

                        TweenMax.allFromTo( _self.menu().menuItems, .35, { opacity:0 }, { opacity:1, ease:Cubic.easeOut }, .06 )
                    
                    ], delay:.6 })
            
                ], 

                paused:true,
                
                onStart: function () {
                    
                },
                
                onComplete: function () {
                   
                    _self.tween = false;
                },
                
                onReverseComplete: function () {
                
                    _self.tween = false; 
                    
                } 
            });

            // filter
            _self.filterTimeline = new TimelineMax({ 

                tweens:[
                
                    //filter Container animation
                    TweenMax.to( _self.filter().filterContainer, .7, {x:'0%', force3D:true, ease:Cubic.easeInOut }) ,
                    
                    //filter Items animation
                    new TimelineMax({ tweens:[
                        
                        // TweenMax.allFrom( _self.filter().filterItems, .35, { x:'100%', ease:Cubic.easeOut }, .06 ),

                        // TweenMax.allFromTo( _self.filter().filterItems, .35, { opacity:0 }, { opacity:1, ease:Cubic.easeOut }, .06 ),

                        TweenMax.to( _self.filter().filterText, .7, { text:"Close", ease:Cubic.easeInOut, color:"#000000" }, .06)
                    
                    ], delay:.6 })
            
                ], 

                paused:true,
                
                onStart: function () {
                    
                },
                
                onComplete: function () {
                   
                    _self.tween = false;
                },
                
                onReverseComplete: function () {
                
                    _self.tween = false; 
                    
                } 
            });
            

        },
        menu: function () {

            var _self     = this;
            var _menuObj  = {};

            _menuObj.menuIconOpen = $('#unlabel-menu-open'),

            _menuObj.menuIconClose = $('#unlabel-menu-close'),

            _menuObj.menuContainer = $('#menu'),

            _menuObj.menuItems = $('#menu ul li'),

            _menuObj.open = function() {
                
                _self.menuToggle = true;
                _self.tween = true;

                _self.panelTimeline.play();
            
            },
    
            _menuObj.close = function() {
                
                _self.menuToggle = !_self.menuToggle;
                _self.tween = true;

                _self.panelTimeline.reverse();
            }
 
            return _menuObj;

        },
        filter: function () {

            var _self     = this;
            var _filterObj  = {};

            _filterObj.filterOpen = $('#unlabel-filter-open');

            _filterObj.filterContainer = $('#filter');

            _filterObj.filterText = $('#unlabel-filter-open .text');

            // _filterObj.filterItems = $('#filter div');

            _filterObj.open = function() {
                _filterObj.filterOpen.on(eventType, function( event ) {
                    
                    var target = typeof event === 'undefined' ? _self.filterToggle : $(event.currentTarget);
                    
                    if( target.attr('id') == 'unlabel-filter-open' ) {
                        
                        event.preventDefault();
                        
                        if (!_self.filterToggle) {
                            
                            _self.filterToggle = true;
                            _self.tween = true;

                            if( _self.menuToggle == true ) {
                                _self.menu().close();
                            }

                            _self.filterTimeline[_self.filterToggle ? 'play' : 'reverse']();
                        } else {

                            _filterObj.close();

                        }
                    }
                });
            }
            
            _filterObj.close = function() {

                _self.filterToggle = !_self.filterToggle;
                _self.tween = true;
                
                _self.filterTimeline.reverse();
            }

            return _filterObj;

        },
        toggle:function() {
            
            var _self = this;

            _self.filter().open();

            _self.menu().menuIconOpen.on(eventType, function( event ) {
                event.preventDefault();
                
                _self.menu().open();
                
                if( _self.filterToggle == true ) {
                    
                    _self.filter().close();
                
                }
            });

            _self.menu().menuIconClose.on(eventType, function( event ) {
                
                event.preventDefault();

                _self.menu().close();
            });

        }
    },
    core.filter = {
        init: function() {
            this.filterGender();
            // this.reset();
        },
        
        labelGridElement:$('#unlabelBrands .labels'),
        radioGender: $('.menu-filter [name=radioButton-Gender]'),
        radioCategories: $('.menu-filter [name=radioButton-Categories]'),
        resetButton: $("#filterClear"),

        labelGrid:function() {
            var _self = this;

            var labelArr = [];
            
            _self.labelGridElement.each(function(index, value) {
                var $labelVal = $(value)
                labelArr.push($labelVal);
            });

            return labelArr;
        },
        filterGender:function() {
            var _self = this;

            //grid of labels
            var labelsGridArray = _self.labelGrid();
            
            //get local storage of choices from filter menu
            var getGenderVal = localStorage.getItem('gender');


            function GridConnector( controls, elements ) {
                //controls
                var filterAll = controls.data('all');
                var filterMenswear = controls.data('men');
                var filterwomenswear = controls.data('women');

                //loop through all elements from an attached grid of elements
                //this will be independent of the controls
                for(var i = 0; i < elements.length; i++) {

                    //grid atrributes
                    var labels = elements[i];
                    var labelMenswear = labels.data('menswear');
                    var labelWomenswear = labels.data('womenswear');

                    //connect controls to grid of elements to display and hide labels
                    //based on filter selections
                    if ( filterAll == 'All' && filterAll != undefined ) {
                        $(labels).removeClass('gone');
                    } else {
                        if( ( filterMenswear != labelMenswear ) && ( filterwomenswear != labelWomenswear ) ) {
                            $(labels).addClass('gone');
                        } else {
                            $(labels).removeClass('gone');
                        }
                    }  
                }
            }
            
            _self.radioGender.each(function( index, value ) {
               var $gender = $(value);
               var radioVal = $gender.val();

                if( getGenderVal == radioVal ) {
                    
                    $gender.prop('checked', true);
                    
                    GridConnector( $gender, labelsGridArray);
                }

                $gender.on('change', function(){
                    $currentRadioVal = $(this).val();
                    
                    localStorage.setItem('gender', $currentRadioVal);
                });

                $gender.on(eventType, function( event ) {

                    var $this = $(this);

                    GridConnector( $this, labelsGridArray);
               
                });
            }); 
        },
        filterCategories:function() {
            var _self = thisl
            
            _self.radioCategories.each(function( index, value ) {
               var $categories = $(value);
    
                $categories.on(eventType, function( event ) {

                    var categoryVal = $categories.val();

                    for(var i = 0; i < _self.labelsGridArray.length; i++) {

                        var labels = _self.labelsGridArray[i];
                        var labelGridCategory = labels.data('category');

                        if( ( categoryVal != _self.labelGridCategory )  ) {
                            labels.addClass('gone');
                        } else {
                            labels.removeClass('gone');
                        }
                    }
                });
            }); 
        
        },
        reset:function() {
            var _self = this;

            _self.resetButton.on(eventType, function( event ) {
                $(".menu-filter [name*='radioButton-']").removeAttr("checked");

                $("#all-gender").attr('checked','')
                
                _self.labelGridElement.removeClass('gone');
            })
        }
    },
    core.toggleApi = {
        
        influencerPanel: {
            win: $(window),

            tween: false,

            influencerPanelToggle: false,

            init:function() {
                this.create();
                this.toggle();
            },
            create:function() {
                
                var _self = this;

                _self.influencerPanelTimeline = new TimelineMax({ 

                    tweens:[
                    
                        TweenMax.to( _self.influencer().influencerPanelContainer, .7, {y:'0%', force3D:true, ease:Cubic.easeInOut }) ,
                        
                        new TimelineMax({ tweens:[
                            
                            TweenMax.allFrom( _self.influencer().influencerPanelItems, .35, { x:'-100%', ease:Cubic.easeOut }, .06 ),

                            TweenMax.allFromTo( _self.influencer().influencerPanelItems, .35, { opacity:0 }, { opacity:1, ease:Cubic.easeOut }, .06 )
                        
                        ], delay:.6 })
                
                    ], 

                    paused:true,
                    
                    onStart: function () {
                        
                    },
                    
                    onComplete: function () {
                       
                        _self.tween = false;
                    },
                    
                    onReverseComplete: function () {
                    
                        _self.tween = false; 
                        
                    } 
                });

            },
            influencer: function () {

                var _self     = this;
                var _coreObj  = {};

                _coreObj.influencerPanelOpen = $('#influencerPanel-open'),

                _coreObj.influencerPanelClose = $('#influencerPanel-close'),

                _coreObj.influencerPanelContainer = $('#influencerPanel'),

                _coreObj.influencerPanelItems = $('#influencerPanel ul li'),

                _coreObj.open = function() {
                    
                    _self.influencerPanelToggle = true;
                    _self.tween = true;

                    _self.influencerPanelTimeline.play();
                },
        
                _coreObj.close = function() {
                    
                    _self.influencerPanelToggle = !_self.influencerPanelToggle;
                    _self.tween = false;

                    _self.influencerPanelTimeline.reverse();
                }
     
                return _coreObj;

            },
            toggle:function() {
                
                var _self = this;

                _self.influencer().influencerPanelOpen.on(eventType, function( event ) {
                    
                    event.preventDefault();
                    
                    _self.influencer().open();
                    
                });

                _self.influencer().influencerPanelClose.on(eventType, function( event ) {
                    
                    event.preventDefault();

                    _self.influencer().close();
                });

            }
        }
    },
    core.googleEvents = {
        init:function() {
            this.influencers();
            this.menu();
            this.filter();
            this.brand();
            this.brandWebsite();
        },
        influencers: function() {
            var influencerCard = $('.influencer-wrapper').children();

            influencerCard.on('click', '.influencer-insta a', function( event ) {

                var $this = $(this)
            
                var influencerHandle = $this.text();

                try {
                    ga('send', 'event', 'click', influencerHandle + 'instgram link was clicked!');  
                    
                } catch(e) {
                    console.error(influencerHandle + 'instagram link click not tracked.');

                }

            }).on('click', '.influencer-choice a', function( event ) {
                var $this = $(this)
            
                var brandName = $this.text();

                try {
                    ga('send', 'event', 'click', brandName + 'link was clicked!');  
                    
                } catch(e) {
                    
                    console.error(brandName + 'link click not tracked.');

                }
            }).on('click', '.influencer-alert a', function( event ) {

                try {
                    ga('send', 'event', 'click','influencer download link was clicked!');  
                    
                } catch(e) {
                    console.error(brandName + 'influencer download link click not tracked.');

                }
            });

        },
        menu:function() {
            var menuLinks  = $('#menu ul.links li a span');
            var menuButton = $('#unlabel-menu-open');

            menuButton.on(eventType, function( event ) {
                try {
                    ga('send', 'event', 'click', 'Menu button was clicked!');  
                } catch(e) {
                    console.error('Menu button click not tracked.');
                }
            });

            menuLinks.on(eventType, function( event ) {
                var $el      = $(this),
                    menuText = $el.text();
                try {
                    ga('send', 'event', 'click', menuText + ' ' + 'link was clicked!');  
                } catch(e) {
                    console.error(menuText + ' ' + 'link click not tracked.');
                }
            }); 
        },
        filter:function() {
            var filterButton = $('#unlabel-filter-open');

            filterButton.on(eventType, function( event ) {
                try {
                    ga('send', 'event', 'click', 'filter button was clicked!');
                } catch(e) {
                    console.error('filter button click not tracked.');
                }
            }); 
        },
        brand:function() {
            var brandLink = $('#unlabelBrands .box-button');

            brandLink.on(eventType, function( event ) {
                var $el = $(this);
                var brandName = $el.data('name');
                
                try {
                    ga('send', 'event', 'click', brandName + 'link on Unlabel was clicked!'); 
                } catch(e) {
                    console.error(brandName + 'link on Unlabel click not tracked.');
                }
            }); 
        },
        brandWebsite:function() {
            var websiteLink = $('.label-about .product-link');
            var websiteLinkWebsite = $('.label-about .product-link-website');

            websiteLink.on(eventType, function( event ) {
                var $el = $(this);
                var websiteName = $el.data('name');
                
                try {
                    ga('send', 'event', 'click', websiteName + 'outbound ios app link was clicked!'); 
                } catch(e) {
                    console.error(websiteName + ' outbound ios app link click not tracked.');
                }
            }); 

            websiteLinkWebsite.on(eventType, function( event ) {
                var $el = $(this);
                var websiteName = $el.data('website-name');
                
                try {
                    ga('send', 'event', 'click', websiteName + 'outbound website link was clicked!'); 
                } catch(e) {
                    console.error(websiteName + ' outbound website link click not tracked.');
                }
            }); 
        } 
    }

    //Return public methods
    return core;

})( UnlabelModule || {}, jQuery );

