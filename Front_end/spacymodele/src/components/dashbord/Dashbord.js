import React, { useEffect, useState } from 'react';
import axios from 'axios';
import MessageAlert from './MessageAlert';
/// https://4x.ant.design/components/table/
import { Card, Space, Statistic, Typography, Table, Input } from 'antd';
import { IdcardOutlined, ShoppingOutlined, UserOutlined } from '@ant-design/icons';

export default function Dashboard() {
  const [statistiques, setStatistiques] = useState({});
  const [dataset, setDataset] = useState([]);
  const [loadingDataset, setLoadingDataset] = useState(true);

  const lowStockMessages = dataset
    .filter(item => item.stock < 10)
    .map(item => `${item.Nom} - Stock: ${item.stock}`);

  useEffect(() => {
    const fetchStatistiques = async () => {
      try {
        const response = await axios.get('http://localhost:5000/statistiques');
        setStatistiques(response.data);
      } catch (error) {
        console.error('Erreur lors de la récupération des statistiques:', error);
      }
    };

    const fetchDataset = async () => {
      try {
        const response = await axios.get('http://localhost:5000/dataset');
        setDataset(response.data);
        setLoadingDataset(false);
      } catch (error) {
        console.error('Erreur lors de la récupération du dataset:', error);
      }
    };

    fetchStatistiques();
    fetchDataset();
  }, []);

  return (
    <div className='container' style={{ padding: 20 }}>
      <Typography.Title level={2}>Prestige Boutique</Typography.Title>
      <Space direction='horizontal'>
        <DashCard
          icon={<ShoppingOutlined style={{ color: 'green', backgroundColor: 'rgba(0,255,0,0.25)', borderRadius: 20, fontSize: 24, padding: 8 }} />}
          title={"Produits"}
          value={statistiques.product}
        />
        <DashCard
          icon={<IdcardOutlined style={{ color: 'purple', backgroundColor: 'rgba(0,255,255,0.25)', borderRadius: 20, fontSize: 24, padding: 8 }} />}
          title={"Fournisseur"}
          value={statistiques.fournisseurs}
        />
        <DashCard
          icon={<UserOutlined style={{ color: 'blue', backgroundColor: 'rgba(0,0,255,0.25)', borderRadius: 20, fontSize: 24, padding: 8 }} />}
          title={"Client"}
          value={statistiques.clients}
        />
      </Space><br/>
      <Space style={{ marginTop: 30 }}>
        <MessageAlert messages={lowStockMessages} />
      </Space><br/>
      <Space style={{ marginTop: 30 }}>
        <DetailProduct loading={loadingDataset} dataset={dataset} />
      </Space>
    </div>
  );

  function DashCard({ title, value, icon }) {
    return (
      <Card>
        <Space direction='horizontal'>
          {icon}
          <Statistic title={title} value={value} />
        </Space>
      </Card>
    );
  }

  function DetailProduct({ loading, dataset }) {
    const [filteredData, setFilteredData] = useState(dataset);
    const { Search } = Input;
    const handleSearch = (value) => {
      const filteredDataset = dataset.filter(item =>
        item.Nom.toLowerCase().includes(value.toLowerCase())
      );
      setFilteredData(filteredDataset);
    };
    return (
      <>
        <Typography.Title level={4}>Details des Produits de la boutique</Typography.Title>
        {/* Input pour faire la recherche par Nom de produit */}
        <Search
          placeholder="Rechercher par nom de produit"
          onSearch={handleSearch}
          style={{ width: 200, marginBottom: 16 }}
        />
        <Table
          columns={[
            {
              title: "Nom",
              dataIndex: "Nom",
              sorter: (a, b) => a.Nom.localeCompare(b.Nom),
              sortDirections: ['ascend', 'descend'],
            },
            {
              title: "Prix Unitaire",
              dataIndex: "price",
              sorter: (a, b) => a.price - b.price,
              sortDirections: ['ascend', 'descend'],
            },
            {
              title: "Quantité entrée",
              dataIndex: "stentree"
            },
            {
              title: "Quantité sortie",
              dataIndex: "stsortie"
            },
            {
              title: "Stock",
              dataIndex: "stock",
              sorter: (a, b) => a.stock - b.stock,
              sortDirections: ['ascend', 'descend'],
              render: (text, record) => {
                // Appliquer une classe conditionnelle basée sur la valeur du stock
                const stockClassName = record.stock <= 10 ? 'low-stock' : '';
                return <span className={stockClassName}>{text}</span>;
              },
            },
          ]}
          loading={loading}
          dataSource={filteredData.map(item => ({
            ...item,
            key: item.Nom, // Remplacez "id" par la propriété réelle de votre dataset qui représente une clé unique
          }))}
        />
      </>
    );
  };
};
