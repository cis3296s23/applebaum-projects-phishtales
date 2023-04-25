import {chrome} from 'jest-chrome';

import {getDomain, updateIgnoreList, getIgnore} from './domainUtil.js'


it('valid domain returned from URL', () => {
   // expect.assertions(1);
    return expect(getDomain("https://github.com/cis3296s23/applebaum-projects-phishtales")).toBe('github.com');
  });


  it('updates ignore list', () => {
    //expect.assertions(1);
    updateIgnoreList(getDomain("https://github.com/cis3296s23/applebaum-projects-phishtales"), true);


    return expect(getIgnore(getDomain("https://github.com/cis3296s23/applebaum-projects-phishtales"))).toBe(0);
  });


  it('removes from ignore list', () => {
    //expect.assertions(1);
    var domain = getDomain("https://github.com/cis3296s23/applebaum-projects-phishtales");
    updateIgnoreList(domain, true);
    expect(getIgnore(domain)).toBe(0);
    updateIgnoreList(domain, false);

    return expect(getIgnore(domain)).toBe(1);
  });