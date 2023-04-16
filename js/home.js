const toggleFilterPage = () => {
    //console.log(document.getElementsByClassName('foreclosure-archive-filter'));
    var element = document.getElementsByClassName('foreclosure-archive-filter')[0],
    style = window.getComputedStyle(element),
    current_max_height = style.getPropertyValue('max-height');
    console.log(top);
    
    if(current_max_height == '50%'){
        document.getElementsByClassName('foreclosure-archive-filter')[0].style.maxHeight = '0%';
        document.getElementsByClassName('foreclosure-archive-filter')[0].style.borderBottom = '0px';
        document.getElementsByClassName('foreclosure-archive-results')[0].style.maxHeight = '100%';
    }
    else{
        document.getElementsByClassName('foreclosure-archive-filter')[0].style.maxHeight = '50%';
        document.getElementsByClassName('foreclosure-archive-filter')[0].style.borderBottom = '1px solid black';
        document.getElementsByClassName('foreclosure-archive-results')[0].style.maxHeight = '50%';
    }
    
}