import type {ReactNode} from 'react';
import {Link,useLocation} from 'react-router-dom';
/** Preserve the route when a section anchor is inside a HashRouter URL. */
export default function SectionLink({id,className,children}:{id:string;className?:string;children:ReactNode}) {
 const location=useLocation();
 return <Link className={className} to={{pathname:location.pathname,search:location.search,hash:`#${id}`}}
   onClick={()=>requestAnimationFrame(()=>document.getElementById(id)?.scrollIntoView())}>{children}</Link>;
}
