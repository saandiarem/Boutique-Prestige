import React, { useState} from 'react';
import { useNavigate } from 'react-router-dom';
import {
  ToolFilled,
  PieChartOutlined,
  IdcardFilled,
  ContactsFilled,
  HddFilled,
  SecurityScanFilled,
  PoweroffOutlined
} from '@ant-design/icons';
import { Layout, Menu} from 'antd';
import Approuter from '../approuter/Approuter';
const { Sider } = Layout;
function getItem(label, key, icon, children) {
  return {
    key,
    icon,
    children,
    label,
  };
}

const Sidebar = ({ setIsAuthenticated }) => {
  const [collapsed, setCollapsed] = useState(false);
  const navigate = useNavigate();
  
  
  const items = [
    getItem('Dashbord', '/dashbord', <PieChartOutlined />),
    getItem('Manage', 'sub1', <ToolFilled />, [
      getItem('Fournisseur', '/manageFournisseur', <IdcardFilled/>),
      getItem('Client', '/manageClient', <ContactsFilled/>),
      getItem('Product', '/addProduct',<HddFilled/>)
    ]),
    getItem('Sante', '/checkDisease', <SecurityScanFilled />),
    getItem('Deconnection', '/', <PoweroffOutlined />),
  ];
  return (
    <Layout
      style={{
        minHeight: '100vh',
      }}
    >
      <Sider collapsible collapsed={collapsed} onCollapse={(value) => setCollapsed(value)}>
        <div className="demo-logo-vertical" />
        <Menu 
        onClick={({key})=>{
          if (key === '/') {
            setIsAuthenticated(false);
          }
          navigate(key)
        }}
        theme="dark" defaultSelectedKeys={['/dashbord']} mode="inline" items={items} />
      </Sider>
      <Layout style={{
            margin: '0 16px',
          }}>
        
          <Approuter/>
        
      </Layout>
    </Layout>
  );
};
export default Sidebar;