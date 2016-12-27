var preloaderWrap = $('.preloader-wrap');
var pageSweeper = $('.page-sweeper');

function dataActiveOn(e) {
    e.attr("data-active", "on")
}

function dataActiveOff(e) {
    e.attr("data-active", "off")
}

function pageLinkTransition(e) {
    pageSweeper.show(), setTimeout(function() {
        dataActiveOn(pageSweeper), setTimeout(function() {
            location.href = e
        }, 750)
    }, 10)
}

function preloaderOff() {
    dataActiveOff(preloaderWrap), setTimeout(function() {
        preloaderWrap.remove()
    }, 1e3);
}

$("a").click(function(e) {
    thisTarget = $(this).attr("target"), 
    thisHref = $(this).attr("href"), 
    "_blank" != thisTarget && 
    -1 == thisHref.indexOf("mailto") && 
    thisHref != "javascript:void(0);" && 
    thisHref != "#influencers" && 
    thisHref != "#unlabelBrandInvite" &&
    thisHref != "#unlabelBrands" && 
    thisHref != "#brandInfo" &&
    thisHref != "http://eepurl.com/bzBZ3r" && //andriod sign up
    thisHref != "http://eepurl.com/ciXM1T" && //designer sign up
    thisHref != "https://itunes.apple.com/us/app/unlabel-discover-emerging/id1092257876?ls=1&mt=8" && 
    thisHref != "https://itunes.apple.com/us/app/unlabel-discover-emerging/id1092257876?ls=1&mt=8" && 
    (e.preventDefault(), "#" != thisHref &&
        pageLinkTransition(thisHref)
    )
});

preloaderWrap.attr("data-preloader-on", "on");



    // filter
        var filterTimeline = new TimelineMax({ 

            tweens:[
            
                //filter Container animation
                TweenMax.staggerTo( $('.brand-invite-header .header-animate'), 1, {y:'0%', force3D:true, ease:Cubic.easeInOut}, 0.5) ,
                // TweenMax.to( $('.brand-invite-header .header-animate-img'), .7, {y:'0%', force3D:true, ease:Cubic.easeInOut}) 
                
                // //filter Items animation
                new TimelineMax({ tweens:[
                    
                //     TweenMax.allFrom( $('.brand-invite-header h1'), .35, { x:'100%', ease:Cubic.easeOut }, .06 ),

                    // TweenMax.allFromTo( $('.brand-invite-header h1'), .35, { opacity:0 }, { opacity:1, ease:Cubic.easeOut }, .06 ),

                //     // TweenMax.to( _self.filter().filterText, .7, { text:"Close", ease:Cubic.easeInOut, color:"#000000" }, .06)
                
                ], delay:.6 })
        
            ], 

            paused:true
        });



$(window).load(function() {
    console.log('page loaded!');
    
    setTimeout(function() {
        console.log('loader off!');
        preloaderOff();
        filterTimeline.play()
    }, 500);
});
