import aws_cdk as cdk
from aws_cdk import aws_ec2

EIP_ALLOCATION_ID = "eipalloc-xxxxxxxxxxxxxxxxx"  # 既存のEIP Allocation IDを指定する

app = cdk.App()
stack = cdk.Stack(app, "existing-eip-nat-vpc-demo-stack")

# 既存のeipを持ったNatProviderを作成する
nat: aws_ec2.NatProvider = aws_ec2.NatProvider.gateway(
    eip_allocation_ids=[EIP_ALLOCATION_ID],
)

# VPCを作成する
vpc = aws_ec2.Vpc(
    stack,
    "Vpc",
    cidr="10.123.0.0/16",
    max_azs=2,
    nat_gateway_provider=nat,
    subnet_configuration=[
        aws_ec2.SubnetConfiguration(
            name="PublicSubnet",
            subnet_type=aws_ec2.SubnetType.PUBLIC,
        ),
        aws_ec2.SubnetConfiguration(
            name="PrivateSubnet",
            subnet_type=aws_ec2.SubnetType.PRIVATE_WITH_NAT,
        ),
    ],
)

subnet: aws_ec2.PublicSubnet = vpc.select_subnets(subnet_type=aws_ec2.SubnetType.PUBLIC).subnets[0]  # 1つしかない想定

app.synth()
