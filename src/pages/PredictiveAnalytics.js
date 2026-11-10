import React, { useState } from 'react';
import { 
  Card, Row, Col, Select, Button, Table, Progress, Statistic, 
  Tag, Space, Alert, message, Slider, Badge 
} from 'antd';
import { 
  LineChart, Line, AreaChart, Area, BarChart, Bar, XAxis, YAxis, 
  CartesianGrid, Tooltip, Legend, ResponsiveContainer 
} from 'recharts';
import { 
  RobotOutlined, RiseOutlined, AlertOutlined, BulbOutlined, 
  CheckCircleOutlined, ThunderboltOutlined, SyncOutlined 
} from '@ant-design/icons';

const { Option } = Select;

// Predictive Datasets
const waterDemandForecast = [
  { month: 'Jul', actual: 420, predicted: 420, lower: 410, upper: 430 },
  { month: 'Aug', actual: 445, predicted: 445, lower: 430, upper: 460 },
  { month: 'Sep', actual: 460, predicted: 460, lower: 445, upper: 475 },
  { month: 'Oct', actual: 435, predicted: 435, lower: 420, upper: 450 },
  { month: 'Nov', actual: 450, predicted: 450, lower: 435, upper: 465 },
  { month: 'Dec (Pred)', actual: null, predicted: 480, lower: 455, upper: 505 },
  { month: 'Jan (Pred)', actual: null, predicted: 510, lower: 475, upper: 545 },
  { month: 'Feb (Pred)', actual: null, predicted: 525, lower: 485, upper: 565 }
];

const budgetExhaustionForecast = [
  { department: 'Public Works', currentSpent: 76, projectedYearEnd: 104, riskLevel: 'High Risk', overrun: '+$180,000' },
  { department: 'Health & Sanitation', currentSpent: 77.5, projectedYearEnd: 98, riskLevel: 'Normal', overrun: '-$64,000' },
  { department: 'Transportation', currentSpent: 75, projectedYearEnd: 108, riskLevel: 'Critical Risk', overrun: '+$168,000' },
  { department: 'Education', currentSpent: 70, projectedYearEnd: 94, riskLevel: 'Normal', overrun: '-$90,000' },
  { department: 'IT & Digital Services', currentSpent: 72, projectedYearEnd: 96, riskLevel: 'Normal', overrun: '-$38,000' }
];

const aiRecommendations = [
  {
    id: 1,
    title: 'Pre-allocate 4 Suction Water Tankers to Ward 2 Basin',
    department: 'Public Works',
    reason: 'Heavy rainfall pattern matching 2024 flood vector predicts 84% drainage choke probability on Nov 15.',
    impact: 'Prevents 120+ citizen water-logging complaints and saves est. $45,000 in emergency repair.',
    confidence: 92,
    status: 'Pending Review'
  },
  {
    id: 2,
    title: 'Shift 3 Transit Buses from Route 14 to Industrial Express Line',
    department: 'Transportation',
    reason: 'Morning peak overcrowding on Route 88 forecast to exceed safety limit by 24% next Monday.',
    impact: 'Reduces commute wait time by 9.5 mins for 4,200 daily passengers.',
    confidence: 88,
    status: 'Pending Review'
  },
  {
    id: 3,
    title: 'Order Buffer Stock of Water Chlorination Tablets',
    department: 'Health & Sanitation',
    reason: 'Seasonal microbial index escalation detected in tributary feeder line #4.',
    impact: 'Guarantees uninterrupted compliance with WHO potable water guidelines.',
    confidence: 96,
    status: 'Approved'
  }
];

const PredictiveAnalytics = () => {
  const [modelType, setModelType] = useState('resource_demand');
  const [selectedDept, setSelectedDept] = useState('All');
  const [recs, setRecs] = useState(aiRecommendations);

  const handleApproveRec = (id) => {
    setRecs(recs.map(r => r.id === id ? { ...r, status: 'Approved' } : r));
    message.success('Recommendation approved and transmitted to dispatch queue.');
  };

  const budgetColumns = [
    { title: 'Department', dataIndex: 'department', key: 'department', render: t => <strong>{t}</strong> },
    { 
      title: 'Current Spent %', 
      dataIndex: 'currentSpent', 
      key: 'currentSpent', 
      render: p => <Progress percent={p} size="small" /> 
    },
    { 
      title: 'Projected FY End %', 
      dataIndex: 'projectedYearEnd', 
      key: 'projectedYearEnd',
      render: v => <span style={{ fontWeight: 600, color: v > 100 ? '#f5222d' : '#52c41a' }}>{v}%</span>
    },
    { 
      title: 'Fiscal Risk Rating', 
      dataIndex: 'riskLevel', 
      key: 'riskLevel',
      render: r => <Tag color={r.includes('Critical') ? 'red' : r.includes('High') ? 'orange' : 'green'}>{r}</Tag>
    },
    { 
      title: 'Projected Variance', 
      dataIndex: 'overrun', 
      key: 'overrun',
      render: o => <span style={{ color: o.startsWith('+') ? '#cf1322' : '#389e0d' }}>{o}</span>
    }
  ];

  return (
    <div style={{ padding: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px', flexWrap: 'wrap', gap: 12 }}>
        <div>
          <h1 style={{ margin: 0, fontSize: 24 }}>AI Predictive Analytics & Demand Forecasting</h1>
          <span style={{ color: '#8c8c8c' }}>Machine learning projections, resource demand curves, and prescriptive district recommendations</span>
        </div>
        <Space wrap>
          <Select value={modelType} onChange={setModelType} style={{ width: 240 }}>
            <Option value="resource_demand">📈 Civic Resource Demand ML</Option>
            <Option value="budget_burn">💰 Budget Burn-Rate ML Model</Option>
            <Option value="grievance_risk">⚠️ Citizen Incident Spike Model</Option>
          </Select>
          <Select value={selectedDept} onChange={setSelectedDept} style={{ width: 180 }}>
            <Option value="All">All Departments</Option>
            <Option value="Public Works">Public Works</Option>
            <Option value="Health & Sanitation">Health & Sanitation</Option>
            <Option value="Transportation">Transportation</Option>
          </Select>
          <Button icon={<SyncOutlined />} onClick={() => message.success('Re-computed AI neural weights with latest telemetry')}>Re-run Models</Button>
        </Space>
      </div>

      <Row gutter={[16, 16]} style={{ marginBottom: '24px' }}>
        <Col xs={24} sm={12} lg={6}>
          <Card bordered={false} style={{ background: '#f9f0ff', borderColor: '#d3adf7' }}>
            <Statistic
              title="Forecasting Accuracy"
              value={94.6}
              precision={1}
              suffix="%"
              prefix={<RobotOutlined style={{ color: '#722ed1' }} />}
              valueStyle={{ color: '#531dab', fontWeight: 600 }}
            />
            <div style={{ marginTop: 8, fontSize: 13, color: '#722ed1' }}>Validated against 24-month backtests</div>
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card bordered={false} style={{ background: '#fff1f0', borderColor: '#ffa39e' }}>
            <Statistic
              title="Critical Bottlenecks Predicted"
              value={2}
              suffix="departments"
              prefix={<AlertOutlined style={{ color: '#f5222d' }} />}
              valueStyle={{ color: '#cf1322', fontWeight: 600 }}
            />
            <div style={{ marginTop: 8, fontSize: 13, color: '#f5222d' }}>Public Works & Transit FY overrun</div>
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card bordered={false} style={{ background: '#e6f7ff', borderColor: '#91d5ff' }}>
            <Statistic
              title="Peak Utility Demand Window"
              value="Dec 15 - Jan 10"
              prefix={<ThunderboltOutlined style={{ color: '#1890ff' }} />}
              valueStyle={{ color: '#096dd9', fontWeight: 600, fontSize: 20 }}
            />
            <div style={{ marginTop: 8, fontSize: 13, color: '#1890ff' }}>+16% projected water & heating load</div>
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card bordered={false} style={{ background: '#f6ffed', borderColor: '#b7eb8f' }}>
            <Statistic
              title="Actionable AI Directives"
              value={recs.filter(r => r.status === 'Pending Review').length}
              suffix="pending"
              prefix={<BulbOutlined style={{ color: '#52c41a' }} />}
              valueStyle={{ color: '#389e0d', fontWeight: 600 }}
            />
            <div style={{ marginTop: 8, fontSize: 13, color: '#52c41a' }}>Ready for magistrate authorization</div>
          </Card>
        </Col>
      </Row>

      {/* Main Forecast Chart */}
      <Row gutter={[16, 16]} style={{ marginBottom: '24px' }}>
        <Col xs={24} lg={16}>
          <Card 
            title="Municipal Utility & Resource Consumption Forecast (Next 3 Months)"
            extra={<Tag color="purple">Model: Random Forest Regressor + Prophet</Tag>}
          >
            <div style={{ height: 350 }}>
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={waterDemandForecast}>
                  <defs>
                    <linearGradient id="confidenceBand" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#722ed1" stopOpacity={0.2}/>
                      <stop offset="95%" stopColor="#722ed1" stopOpacity={0.02}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} />
                  <XAxis dataKey="month" />
                  <YAxis domain={[380, 600]} unit="k m³" />
                  <Tooltip />
                  <Legend />
                  <Area type="monotone" dataKey="upper" name="95% Confidence Upper Bound" stroke="#d3adf7" strokeDasharray="3 3" fill="url(#confidenceBand)" />
                  <Area type="monotone" dataKey="lower" name="95% Confidence Lower Bound" stroke="#d3adf7" strokeDasharray="3 3" fill="none" />
                  <Line type="monotone" dataKey="actual" name="Historical Observed Consumption" stroke="#1890ff" strokeWidth={3} dot={{ r: 5 }} />
                  <Line type="monotone" dataKey="predicted" name="AI Projected Trajectory" stroke="#722ed1" strokeWidth={3} strokeDasharray="5 5" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </Card>
        </Col>

        <Col xs={24} lg={8}>
          <Card title="Anomaly Detection Telemetry">
            <Alert
              message="Ward 2 Inflow Anomaly Detected"
              description="Water pipeline pressure drop of 24% detected in Ward 2 while demand spiked. Indicates underground rupture probability."
              type="error"
              showIcon
              style={{ marginBottom: 16 }}
            />
            <Alert
              message="Transit Route 14 Density Warning"
              description="Commuter load projected to peak at 134% of bus capacity next Tuesday morning."
              type="warning"
              showIcon
              style={{ marginBottom: 16 }}
            />
            <Alert
              message="Fiscal Balance Alert"
              description="Public Works burn-rate indicates potential budget depletion 38 days before fiscal year close."
              type="info"
              showIcon
            />
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]}>
        <Col xs={24} lg={13}>
          <Card title="Prescriptive AI Directives & Action Plan">
            {recs.map(rec => (
              <Card 
                key={rec.id} 
                type="inner" 
                title={<span><BulbOutlined style={{ color: '#faad14', marginRight: 8 }} />{rec.title}</span>}
                extra={
                  rec.status === 'Approved' ? (
                    <Tag color="green" icon={<CheckCircleOutlined />}>Authorized</Tag>
                  ) : (
                    <Button 
                      type="primary" 
                      size="small" 
                      onClick={() => handleApproveRec(rec.id)}
                    >
                      Authorize Action
                    </Button>
                  )
                }
                style={{ marginBottom: 12 }}
              >
                <div><strong>Reasoning:</strong> {rec.reason}</div>
                <div style={{ marginTop: 4, color: '#389e0d' }}><strong>Impact:</strong> {rec.impact}</div>
                <div style={{ marginTop: 8, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Tag color="blue">{rec.department}</Tag>
                  <span style={{ fontSize: 12, color: '#8c8c8c' }}>Model Confidence: <strong>{rec.confidence}%</strong></span>
                </div>
              </Card>
            ))}
          </Card>
        </Col>

        <Col xs={24} lg={11}>
          <Card title="Fiscal Year-End Budget Exhaustion Projection">
            <Table dataSource={budgetExhaustionForecast} columns={budgetColumns} pagination={false} size="middle" />
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default PredictiveAnalytics;
