import React from 'react';
import { Result, Button } from 'antd';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('ErrorBoundary caught an error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <Result
          status="500"
          title="Something went wrong"
          subTitle="An unexpected error occurred while loading the application."
          extra={
            <Button 
              type="primary" 
              onClick={() => this.setState({ hasError: false })}
            >
              Try Again
            </Button>
          }
        />
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;