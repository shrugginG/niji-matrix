import {Component,type ReactNode} from 'react';
export default class SimulationErrorBoundary extends Component<{children:ReactNode},{error:Error|null}>{
 state:{error:Error|null}={error:null};
 static getDerivedStateFromError(error:Error){return {error};}
 render(){
  if(this.state.error)return <div className="empty" role="alert"><h2>公害仿真暂时无法加载</h2><p>请重新加载页面后重试，本地草稿不会因此被删除。</p><details><summary>查看错误详情</summary><pre style={{whiteSpace:'pre-wrap'}}>{this.state.error.message}</pre></details><button onClick={()=>window.location.reload()}>重新加载</button></div>;
  return this.props.children;
 }
}
